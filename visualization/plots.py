import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

SAVE_DIR = os.path.join(os.path.dirname(__file__))

def generate_plots(df):
    os.makedirs(SAVE_DIR, exist_ok=True)

    plt.style.use("ggplot")

    # 1. Latency Distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["latency"], bins=15, color="#00BFFF", edgecolor="white")
    ax.axvline(df["latency"].mean(), color="red", linestyle="--", label=f"Mean: {df['latency'].mean():.1f}")
    ax.set_title("Latency Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Latency (ms)")
    ax.set_ylabel("Count")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "latency.png"), dpi=150)
    plt.close()

    # 2. PDR per Node
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["green" if p >= 0.8 else "red" for p in df["pdr"]]
    ax.bar(df["node_id"], df["pdr"], color=colors, edgecolor="white")
    ax.axhline(0.8, color="orange", linestyle="--", label="Min Threshold (0.8)")
    ax.set_title("Packet Delivery Ratio per Node", fontsize=14, fontweight="bold")
    ax.set_xlabel("Node ID")
    ax.set_ylabel("PDR")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "pdr.png"), dpi=150)
    plt.close()

    # 3. Energy Consumption
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["node_id"], df["energy"], color="#FF6347", linewidth=1.5, marker="o", markersize=3)
    ax.fill_between(df["node_id"], df["energy"], alpha=0.2, color="#FF6347")
    ax.set_title("Energy Consumption per Node", fontsize=14, fontweight="bold")
    ax.set_xlabel("Node ID")
    ax.set_ylabel("Energy (J)")
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "energy.png"), dpi=150)
    plt.close()

    # 4. Network Lifetime
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df["energy"], df["lifetime"], c=df["pdr"], cmap="RdYlGn", s=60, edgecolors="gray", linewidth=0.5)
    sm = plt.cm.ScalarMappable(cmap="RdYlGn", norm=plt.Normalize(df["pdr"].min(), df["pdr"].max()))
    plt.colorbar(sm, ax=ax, label="PDR")
    ax.set_title("Energy vs Network Lifetime", fontsize=14, fontweight="bold")
    ax.set_xlabel("Energy (J)")
    ax.set_ylabel("Lifetime (s)")
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "lifetime.png"), dpi=150)
    plt.close()

    print(f"  4 charts saved to {SAVE_DIR}")
