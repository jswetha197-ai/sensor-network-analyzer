"""
WSN Streamlit Dashboard
Run with: python -m streamlit run dashboard_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis.analysis   import analyze_data
from visualization.plots import generate_plots
from reports.report      import generate_report
from database.db         import save_to_db

st.set_page_config(page_title="WSN Dashboard", page_icon="📡", layout="wide")
st.title("WSN Performance Dashboard")
st.markdown("---")

# ── Sidebar: Upload CSV only ──────────────────────────────────────────────
st.sidebar.header("⚙️ Controls")
st.sidebar.markdown("### 📤 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

df = None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"✅ Loaded {len(df)} rows")
    
    # Save to database
    save_to_db(df)
    st.sidebar.info("💾 Data saved to database")

    # Node filter
    node_filter = st.sidebar.slider(
        "Filter Node Range",
        1, int(df["node_id"].max()),
        (1, int(df["node_id"].max()))
    )
    df = df[(df["node_id"] >= node_filter[0]) & (df["node_id"] <= node_filter[1])]

else:
    st.info("👈 Upload a CSV file to get started")
    st.stop()

# ── Analysis ──────────────────────────────────────────────────────────────
results = analyze_data(df)

# ── KPI Cards ─────────────────────────────────────────────────────────────
st.subheader("📊 Key Performance Indicators")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Avg PDR",      f"{results['avg_pdr']:.3f}")
c2.metric("Avg Latency",  f"{results['avg_latency']:.1f} ms")
c3.metric("Avg Energy",   f"{results['avg_energy']:.2f} J")
c4.metric("Avg Lifetime", f"{results['avg_lifetime']:.1f} s")
c5.metric("Health Score", f"{results['network_health_score']} / 100")

st.markdown("---")

# ── Alerts ────────────────────────────────────────────────────────────────
st.subheader("⚠️ Network Status")
a1, a2, a3 = st.columns(3)
with a1:
    if results["high_latency_count"] > 0:
        st.warning(f"High latency detected: {results['high_latency_count']} nodes")
    else:
        st.success("✅ Latency normal")
with a2:
    if results["low_pdr_count"] > 0:
        st.error(f"Low PDR: {results['low_pdr_count']} nodes below threshold")
    else:
        st.success("✅ PDR healthy")
with a3:
    if results["critical_energy_count"] > 0:
        st.warning(f"Energy critical: {results['critical_energy_count']} nodes")
    else:
        st.success("✅ Energy OK")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────
st.subheader("📈 Performance Visualizations")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.histogram(df, x="latency", nbins=15,
                        title="Latency Distribution",
                        color_discrete_sequence=["#00BFFF"])
    fig1.add_vline(x=df["latency"].mean(), line_dash="dash",
                   line_color="red", annotation_text="Mean")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    bar_colors = ["green" if p >= 0.8 else "red" for p in df["pdr"]]
    fig2 = go.Figure(go.Bar(x=df["node_id"], y=df["pdr"], marker_color=bar_colors))
    fig2.add_hline(y=0.8, line_dash="dash", line_color="orange", annotation_text="Threshold")
    fig2.update_layout(title="PDR per Node", xaxis_title="Node ID", yaxis_title="PDR")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig3 = px.line(df, x="node_id", y="energy",
                   title="Energy Consumption per Node",
                   color_discrete_sequence=["#FF6347"])
    fig3.update_traces(fill="tozeroy")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(df, x="energy", y="lifetime",
                      color="pdr", size="energy",
                      title="Energy vs Network Lifetime",
                      color_continuous_scale="RdYlGn")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── Data Table ────────────────────────────────────────────────────────────
st.subheader("📋 Raw Dataset")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# ── Generate Report ───────────────────────────────────────────────────────
st.subheader("📄 Generate Report")
st.caption("Create a PDF summary of your WSN analysis")

if st.button("Generate & Download PDF 📥", type="primary"):
    with st.spinner("Creating your report..."):
        try:
            generate_plots(df)
            generate_report(results, df=df)
            reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
            latest = max(
                [f for f in os.listdir(reports_dir) if f.endswith(".pdf")],
                key=lambda f: os.path.getmtime(os.path.join(reports_dir, f))
            )
            report_path = os.path.join(reports_dir, latest)
            with open(report_path, "rb") as f:
                pdf_bytes = f.read()
            st.success("✅ Report generated!")
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name="wsn_report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {e}")