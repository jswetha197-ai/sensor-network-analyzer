"""
REST API for WSN Performance Analysis Tool
Run with: python api/api.py
Endpoints:
  POST /data          - Submit sensor data
  GET  /data          - Get all sensor data
  GET  /analysis      - Get analysis results
  GET  /report        - Download PDF report
"""

from flask import Flask, request, jsonify, send_file
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.db      import save_to_db, load_from_db
from analysis.analysis import analyze_data
from visualization.plots import generate_plots
from reports.report   import generate_report

app = Flask(__name__)
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "report.pdf")

# ── POST /data ─────────────────────────────────────────────────────────────
@app.route("/data", methods=["POST"])
def receive_data():
    """
    Accept JSON like:
    [{"node_id":1,"pdr":0.9,"latency":80,"energy":1.2,"lifetime":500}, ...]
    """
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No JSON payload received"}), 400

        df = pd.DataFrame(payload)
        required = {"node_id", "pdr", "latency", "energy", "lifetime"}
        if not required.issubset(df.columns):
            return jsonify({"error": f"Missing columns. Required: {required}"}), 400

        save_to_db(df)
        return jsonify({"message": f"Saved {len(df)} records successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── GET /data
@app.route("/data", methods=["GET"])
def get_data():
    try:
        df = load_from_db()
        return jsonify(df.to_dict(orient="records")), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── GET /analysis
@app.route("/analysis", methods=["GET"])
def get_analysis():
    try:
        df      = load_from_db()
        results = analyze_data(df)
        # Remove DataFrame objects — not JSON serializable
        safe    = {k: v for k, v in results.items() if not k.startswith("_")}
        return jsonify(safe), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── GET /report
@app.route("/report", methods=["GET"])
def get_report():
    try:
        df      = load_from_db()
        results = analyze_data(df)
        generate_plots(df)
        generate_report(results)
        return send_file(REPORT_PATH, as_attachment=True, download_name="wsn_report.pdf")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(" WSN API running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
