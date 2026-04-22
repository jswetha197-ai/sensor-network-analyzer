import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="WSN Dashboard", layout="wide")

st.title("📡 WSN Performance Dashboard")

# Sidebar
st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Filters
    node_filter = st.sidebar.slider("Select Node Range", 1, int(df["node_id"].max()), (1, int(df["node_id"].max())))
    df = df[(df["node_id"] >= node_filter[0]) & (df["node_id"] <= node_filter[1])]

    # --- KPI CARDS ---
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg PDR", f"{df['pdr'].mean():.2f}")
    col2.metric("Avg Latency", f"{df['latency'].mean():.2f}")
    col3.metric("Avg Energy", f"{df['energy'].mean():.2f}")
    col4.metric("Avg Lifetime", f"{df['lifetime'].mean():.2f}")

    # --- ALERTS ---
    st.subheader("🚨 Alerts")

    high_latency = df[df["latency"] > 150]
    low_pdr = df[df["pdr"] < 0.8]

    if not high_latency.empty:
        st.warning(f"⚠️ {len(high_latency)} nodes have high latency!")

    if not low_pdr.empty:
        st.error(f"❌ {len(low_pdr)} nodes have low PDR!")

    # --- DATA PREVIEW ---
    st.subheader("📋 Data Preview")
    st.dataframe(df, use_container_width=True)

    # --- GRAPHS ---
    st.subheader("📈 Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df, x="latency", title="Latency Distribution", color_discrete_sequence=["#00BFFF"])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(df, x="node_id", y="pdr", title="PDR per Node")
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(df, x="energy", y="lifetime",
                      title="Energy vs Lifetime",
                      color="pdr",
                      size="energy")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("👈 Upload a CSV file from sidebar to start")