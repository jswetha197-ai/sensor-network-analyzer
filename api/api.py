from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/data")
def get_data():
    df = pd.read_csv("data/sensor_data.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/metrics")
def metrics():
    df = pd.read_csv("data/sensor_data.csv")

    results = {
        "avg_pdr": df["pdr"].mean(),
        "avg_latency": df["latency"].mean(),
        "avg_energy": df["energy"].mean(),
        "avg_lifetime": df["lifetime"].mean()
    }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)