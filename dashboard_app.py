
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from visualization.dashboard_style import apply_custom_style

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="WSN Dashboard",
    layout="wide",
    page_icon="📡"
)

# ================= APPLY STYLE =================
apply_custom_style()

# ================= TITLE =================
st.title("📡 WSN Performance Dashboard")
st.markdown("Analyze Wireless Sensor Network performance using uploaded CSV data.")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Sensor Data CSV",
    type=["csv"]
)

# ================= LOAD DATA =================
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# ================= REQUIRED COLUMNS =================
required_columns = ["node_id", "pdr", "latency", "energy", "lifetime"]

for col in required_columns:
    if col not in df.columns:
        st.error(f"Missing required column: {col}")
        st.stop()

# ================= FILTER =================
node_range = st.sidebar.slider(
    "Select Node Range",
    int(df["node_id"].min()),
    int(df["node_id"].max()),
    (
        int(df["node_id"].min()),
        int(df["node_id"].max())
    )
)

filtered_df = df[
    (df["node_id"] >= node_range[0]) &
    (df["node_id"] <= node_range[1])
]

# ================= METRICS =================
st.markdown("---")
st.subheader("📊 Key Metrics")

avg_pdr = filtered_df["pdr"].mean()
avg_latency = filtered_df["latency"].mean()
avg_energy = filtered_df["energy"].mean()
avg_lifetime = filtered_df["lifetime"].mean()

health_score = round((avg_pdr * 100) - (avg_latency / 10), 2)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Avg PDR", f"{avg_pdr:.3f}")
col2.metric("Avg Latency", f"{avg_latency:.1f} ms")
col3.metric("Avg Energy", f"{avg_energy:.2f} J")
col4.metric("Avg Lifetime", f"{avg_lifetime:.1f} s")
col5.metric("Health Score", f"{health_score:.2f} / 100")

# ================= ALERTS =================
st.markdown("---")
st.subheader("🚨 Alerts")

low_pdr_nodes = filtered_df[filtered_df["pdr"] < 0.8]
high_latency_nodes = filtered_df[filtered_df["latency"] > 150]
high_energy_nodes = filtered_df[filtered_df["energy"] > 4]

if len(low_pdr_nodes) > 0:
    st.error(f"{len(low_pdr_nodes)} nodes have LOW PDR")

if len(high_latency_nodes) > 0:
    st.warning(f"{len(high_latency_nodes)} nodes have HIGH LATENCY")

if len(high_energy_nodes) > 0:
    st.warning(f"{len(high_energy_nodes)} nodes have HIGH ENERGY")

# ================= DATA PREVIEW =================
st.markdown("---")
st.subheader("📋 Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# ================= VISUALIZATIONS =================
st.markdown("---")
st.subheader("📈 Visualizations")

chart1, chart2 = st.columns(2)

with chart1:
    fig_latency = px.histogram(
        filtered_df,
        x="latency",
        nbins=15,
        title="Latency Distribution",
        template="plotly_dark"
    )

    fig_latency.add_vline(
        x=150,
        line_dash="dash",
        line_color="red"
    )

    st.plotly_chart(fig_latency, use_container_width=True)

with chart2:
    filtered_df["status"] = filtered_df["pdr"].apply(
        lambda x: "Good" if x >= 0.8 else "Low"
    )

    fig_pdr = px.bar(
        filtered_df,
        x="node_id",
        y="pdr",
        color="status",
        title="PDR Per Node",
        template="plotly_dark",
        color_discrete_map={
            "Good": "green",
            "Low": "red"
        }
    )

    fig_pdr.add_hline(
        y=0.8,
        line_dash="dash",
        line_color="yellow"
    )

    st.plotly_chart(fig_pdr, use_container_width=True)

# ================= SECOND ROW =================
chart3, chart4 = st.columns(2)

with chart3:
    fig_energy = px.area(
        filtered_df,
        x="node_id",
        y="energy",
        title="Energy Consumption",
        template="plotly_dark"
    )

    st.plotly_chart(fig_energy, use_container_width=True)

with chart4:
    fig_scatter = px.scatter(
        filtered_df,
        x="energy",
        y="lifetime",
        size="latency",
        color="pdr",
        hover_data=["node_id"],
        title="Energy vs Lifetime",
        template="plotly_dark"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ================= EXTRA ANALYTICS =================
st.markdown("---")
st.subheader("🔥 Advanced Analytics")

# Correlation Heatmap
corr = filtered_df[["pdr", "latency", "energy", "lifetime"]].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu",
    title="Correlation Heatmap"
)

st.plotly_chart(fig_corr, use_container_width=True)

# Box Plot
fig_box = px.box(
    filtered_df,
    y="latency",
    template="plotly_dark",
    title="Latency Spread"
)

st.plotly_chart(fig_box, use_container_width=True)

# Pie Chart
healthy_nodes = len(filtered_df[filtered_df["pdr"] >= 0.8])
weak_nodes = len(filtered_df[filtered_df["pdr"] < 0.8])

pie_df = pd.DataFrame({
    "Status": ["Healthy", "Weak"],
    "Count": [healthy_nodes, weak_nodes]
})

fig_pie = px.pie(
    pie_df,
    names="Status",
    values="Count",
    template="plotly_dark",
    title="Node Health Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)

# Lifetime Trend
fig_lifetime = px.line(
    filtered_df,
    x="node_id",
    y="lifetime",
    template="plotly_dark",
    title="Lifetime Trend"
)

st.plotly_chart(fig_lifetime, use_container_width=True)

# Radar Chart
fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=[
        avg_pdr * 100,
        100 - (avg_latency / 3),
        100 - (avg_energy * 10),
        avg_lifetime / 10
    ],
    theta=["PDR", "Latency", "Energy", "Lifetime"],
    fill='toself'
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    template="plotly_dark",
    title="Network Radar Analysis"
)

st.plotly_chart(fig_radar, use_container_width=True)

# ================= EXPORT =================
st.markdown("---")
st.subheader("📥 Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv,
    file_name="filtered_sensor_data.csv",
    mime="text/csv"
)
