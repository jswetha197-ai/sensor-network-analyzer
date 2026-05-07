"""
WSN Performance Analysis Tool — Main Runner
Run with: python main.py
"""

import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(__file__))

from analysis.analysis   import analyze_data
from visualization.plots import generate_plots
from reports.report      import generate_report
from database.db         import save_to_db

print("=" * 50)
print("  WSN Performance Analysis Tool")
print("=" * 50)

# ── STEP 1: Generate Data ───────────────────────────────────────────────
print("\n[1/5] Generating sensor data...")
np.random.seed(42)
data = {
    "node_id":  np.arange(1, 51),
    "pdr":      np.round(np.random.uniform(0.65, 1.0, 50), 4),
    "latency":  np.round(np.random.uniform(10, 220, 50), 2),
    "energy":   np.round(np.random.uniform(0.1, 5.5, 50), 4),
    "lifetime": np.round(np.random.uniform(100, 1000, 50), 2),
}
df = pd.DataFrame(data)
print(f"  Generated {len(df)} node records ✅")

# ── STEP 2: Save CSV + DB ───────────────────────────────────────────────
print("\n[2/5] Saving data...")
os.makedirs("data", exist_ok=True)
df.to_csv("data/sensor_data.csv", index=False)
save_to_db(df)
print("  Saved to CSV and database ✅")

# ── STEP 3: Analysis ────────────────────────────────────────────────────
print("\n[3/5] Running analysis...")
results = analyze_data(df)
print(f"\n  {'Metric':<30} {'Value':>10}")
print(f"  {'-'*42}")
for k, v in results.items():
    if not k.startswith("_"):
        print(f"  {k:<30} {v:>10.4f}")

# ── STEP 4: Charts ──────────────────────────────────────────────────────
print("\n[4/5] Generating charts...")
os.makedirs("visualization", exist_ok=True)
generate_plots(df)
print("  Charts saved ✅")

# ── STEP 5: Report ──────────────────────────────────────────────────────
print("\n[5/5] Generating PDF report...")
os.makedirs("reports", exist_ok=True)
generate_report(results)
print("  Report saved → reports/report.pdf ✅")

print("\n" + "=" * 50)
print("  Done! Open reports/report.pdf to view.")
print("  Run: python -m streamlit run dashboard_app.py")
print("=" * 50)
