import numpy as np

def analyze_data(df):
    results = {}

    # Basic metrics
    results["avg_pdr"] = df["pdr"].mean()
    results["avg_latency"] = df["latency"].mean()
    results["avg_energy"] = df["energy"].mean()
    results["avg_lifetime"] = df["lifetime"].mean()

    # ✅ Advanced statistics
    results["std_latency"] = df["latency"].std()
    results["var_energy"] = df["energy"].var()

    # Threshold analysis
    results["high_latency"] = df[df["latency"] > 150]
    results["low_pdr"] = df[df["pdr"] < 0.8]

    return results