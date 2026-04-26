<<<<<<< HEAD
import pandas as pd
import numpy as np

# Imports from your modules
from analysis.analysis import analyze_data
from visualization.plots import generate_plots
from reports.report import generate_report
from database.db import save_to_db

# (Optional dashboard)
# from visualization.dashboard import run_dashboard


# -------- STEP 1: Generate Data -------- #
data = {
    "node_id": np.arange(1, 51),
    "pdr": np.random.uniform(0.7, 1.0, 50),
    "latency": np.random.uniform(10, 200, 50),
    "energy": np.random.uniform(0.1, 5.0, 50),
    "lifetime": np.random.uniform(100, 1000, 50)
}

df = pd.DataFrame(data)

print("Data generated successfully ✅")


# -------- STEP 2: Save Data -------- #
df.to_csv("data/sensor_data.csv", index=False)
print("Data saved as CSV 📄")

# -------- STEP 3: Save to Database -------- #
save_to_db(df)
print("Data saved to database 🗄️")


# -------- STEP 4: Analysis -------- #
results = analyze_data(df)

print("\n--- Analysis Results ---")
print(f"Average PDR: {results['avg_pdr']:.2f}")
print(f"Average Latency: {results['avg_latency']:.2f}")
print(f"Average Energy: {results['avg_energy']:.2f}")
print(f"Average Lifetime: {results['avg_lifetime']:.2f}")

# Advanced stats
print(f"Latency Std Dev: {results['std_latency']:.2f}")
print(f"Energy Variance: {results['var_energy']:.2f}")


# -------- STEP 5: Visualization -------- #
generate_plots(df)
print("Graphs generated 📊")


# -------- STEP 6: Report -------- #
generate_report(results)
print("Report generated 📄")


# -------- STEP 7: Dashboard (Optional) -------- #
# Uncomment if using Plotly dashboard
# run_dashboard()


=======
import pandas as pd
import numpy as np

# Imports from your modules
from analysis.analysis import analyze_data
from visualization.plots import generate_plots
from reports.report import generate_report
from database.db import save_to_db

# (Optional dashboard)
# from visualization.dashboard import run_dashboard


# -------- STEP 1: Generate Data -------- #
data = {
    "node_id": np.arange(1, 51),
    "pdr": np.random.uniform(0.7, 1.0, 50),
    "latency": np.random.uniform(10, 200, 50),
    "energy": np.random.uniform(0.1, 5.0, 50),
    "lifetime": np.random.uniform(100, 1000, 50)
}

df = pd.DataFrame(data)

print("Data generated successfully ✅")


# -------- STEP 2: Save Data -------- #
df.to_csv("data/sensor_data.csv", index=False)
print("Data saved as CSV 📄")

# -------- STEP 3: Save to Database -------- #
save_to_db(df)
print("Data saved to database 🗄️")


# -------- STEP 4: Analysis -------- #
results = analyze_data(df)

print("\n--- Analysis Results ---")
print(f"Average PDR: {results['avg_pdr']:.2f}")
print(f"Average Latency: {results['avg_latency']:.2f}")
print(f"Average Energy: {results['avg_energy']:.2f}")
print(f"Average Lifetime: {results['avg_lifetime']:.2f}")

# Advanced stats
print(f"Latency Std Dev: {results['std_latency']:.2f}")
print(f"Energy Variance: {results['var_energy']:.2f}")


# -------- STEP 5: Visualization -------- #
generate_plots(df)
print("Graphs generated 📊")


# -------- STEP 6: Report -------- #
generate_report(results)
print("Report generated 📄")


# -------- STEP 7: Dashboard (Optional) -------- #
# Uncomment if using Plotly dashboard
# run_dashboard()


>>>>>>> e63dc3f91ad5a28854fe683ce3a0849134189c32
print("\n🎉 Project executed successfully!")