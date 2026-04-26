# 📡 WSN Analytics Dashboard

An **Automated Performance Analysis Tool** for Wireless Sensor Networks (WSN) that collects, processes, and visualizes network performance metrics.

---

## 🚀 Features

- 📂 Upload sensor data (CSV)
- 📊 Interactive dashboard (Streamlit)
- 📈 Performance metrics:
  - Packet Delivery Ratio (PDR)
  - Latency
  - Energy Consumption
  - Network Lifetime
- 📉 Advanced statistical analysis:
  - Standard deviation
  - Variance
- 🗄️ SQL database integration (SQLite)
- 📄 Automated report generation (PDF)
- 📡 REST API support (Flask ready)
- 📊 Beautiful visualizations using Plotly

---

## 🧰 Technologies Used

- Python
- Pandas / NumPy
- Matplotlib / Plotly
- Streamlit
- SQLite (SQLAlchemy)
- Flask (REST API)
- ReportLab (PDF generation)

---

## 📂 Project Structure

- `pro/`
  - `main.py`                 # Main execution script
  - `dashboard_app.py`        # Streamlit dashboard
  - `analysis.py`             # Data analysis logic
  - `plots.py`                # Visualization functions
  - `report.py`               # PDF report generation
  - `db.py`                   # Database handling
  - `convert_kaggle.py`       # Dataset conversion script
  - `sensor_data.csv`         # Sample dataset
  - `kaggle_converted.csv`    # Processed dataset
  - `requirements.txt`        # Dependencies



---

## ▶️ Run the Project

### Run dashboard
```bash
streamlit run dashboard_app.py
Run analysis:
python main.py
📊 Input Data Format

CSV should contain columns like:

node_id
pdr
latency
energy
lifetime

💡 Future Improvements
Live IoT data integration
Cloud deployment
Machine learning predictions
Real-time monitoring
