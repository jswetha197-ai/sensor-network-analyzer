def apply_custom_style():
    return """
    <style>
    /* Main background */
    .stApp {
        background-color: #0b1020;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b2e;
        border-right: 1px solid #2b2f45;
    }

    /* Metric Cards */
    .metric-card {
        background: #1c2238;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }

    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
    }

    /* Upload Box */
    .stFileUploader {
        background-color: #1c2238;
        border-radius: 10px;
        padding: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #ff4b6e;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 15px;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """