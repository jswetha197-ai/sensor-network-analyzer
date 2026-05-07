import numpy as np
from scipy import stats

def analyze_data(df):
    results = {}

    # Basic metrics
    results["avg_pdr"]      = df["pdr"].mean()
    results["avg_latency"]  = df["latency"].mean()
    results["avg_energy"]   = df["energy"].mean()
    results["avg_lifetime"] = df["lifetime"].mean()

    # Advanced statistics
    results["std_latency"]  = df["latency"].std()
    results["var_energy"]   = df["energy"].var()
    results["min_pdr"]      = df["pdr"].min()
    results["max_pdr"]      = df["pdr"].max()
    results["median_latency"] = df["latency"].median()

    # Network health score (0-100)
    pdr_score      = df["pdr"].mean() * 100
    latency_score  = max(0, 100 - (df["latency"].mean() / 2))
    energy_score   = max(0, 100 - (df["energy"].mean() * 10))
    results["network_health_score"] = round((pdr_score + latency_score + energy_score) / 3, 2)

    # Threshold analysis (counts only — safe for report)
    results["high_latency_count"] = int((df["latency"] > 150).sum())
    results["low_pdr_count"]      = int((df["pdr"] < 0.8).sum())
    results["critical_energy_count"] = int((df["energy"] > 4.0).sum())

    # Keep full DataFrames separately (not passed to report)
    results["_high_latency_df"] = df[df["latency"] > 150]
    results["_low_pdr_df"]      = df[df["pdr"] < 0.8]

    return results
