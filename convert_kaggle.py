import pandas as pd
import numpy as np

# Load dataset (IMPORTANT: separator is ;)
df = pd.read_csv("data/household_power_consumption.txt", sep=';', low_memory=False)

# Remove missing values
df = df.dropna()

# Convert columns to numeric
df["Global_active_power"] = pd.to_numeric(df["Global_active_power"], errors='coerce')
df["Global_intensity"] = pd.to_numeric(df["Global_intensity"], errors='coerce')
df["Voltage"] = pd.to_numeric(df["Voltage"], errors='coerce')

df = df.dropna()

# Take only first 200 rows (for performance)
df = df.head(200)

# Create your project format
new_df = pd.DataFrame({
    "node_id": range(1, len(df)+1),
    "pdr": np.random.uniform(0.7, 1.0, len(df)),
    "latency": df["Global_intensity"],
    "energy": df["Global_active_power"],
    "lifetime": df["Voltage"]
})

# Save new dataset
new_df.to_csv("data/kaggle_converted.csv", index=False)

print("Converted dataset ready ✅")