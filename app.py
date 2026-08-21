import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="StockFlow",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# MODERN CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.15), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(6, 182, 212, 0.12), transparent 25%),
            linear-gradient(135deg, #080b14 0%, #101629 100%);
        color: #f8fafc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(13, 18, 33, 0.92);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: Arial, sans-serif;
    }

    /* Hero */
    .hero {
        padding: 35px 40px;
        border-radius: 28px;
        background: linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.9),
            rgba(6, 182, 212, 0.65)
        );
        margin-bottom: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    }

    .hero-title {
        font-size: 46px;
        font-weight: 800;
        color: white;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 18px;
        color: rgba(255,255,255,0.8);
        margin-top: 8px;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.09);
        backdrop-filter: blur(16px);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 15px;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.025)
        );
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 22px;
        padding: 22px;
        min-height: 120px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.18);
    }

    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
    }

    .positive {
        color: #22c55e;
    }

    .negative {
        color: #ef4444;
    }

    /* Section title */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Streamlit buttons */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 0;
        padding: 12px 18px;
        font-weight: 700;
        background: linear-gradient(135deg, #7c3aed, #06b6d4);
        color: white;
        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(124,58,237,0.35);
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

@st.cache_data
def generate_market_data(days=250):

    np.random.seed(42)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=days,
        freq="B"
    )

    returns = np.random.normal(0.0007, 0.018, days)

    close = 100 * np.exp(np.cumsum(returns))

    open_price = np.zeros(days)
    open_price[0] = close[0]

    for i in range(1, days):
        open_price[i] = close[i - 1] * np.random.uniform(0.985, 1.015)

    high = np.maximum(open_price, close) * np.random.uniform(1.002, 1.03, days)
    low = np.minimum(open_price, close) * np.random.uniform(0.97, 0.998, days)

    volume = np.random.randint(500_000, 5_000_000, days)

    return pd.DataFrame({
        "Date": dates,
        "Open": open_price,
        "High": high,
        "Low": low,
        "Close": close,
        "Volume": volume
    })


df = generate_market_data()


# =========================================================
# CALCULATIONS
# =========================================================

def calculate_rsi(series, period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def calculate_macd(series):

    ema_fast = series.ewm(span=12, adjust=False).mean()
    ema_slow = series.ewm(span=26, adjust=False).mean()

    macd = ema_fast - ema_slow
    signal = macd.ewm(span=9, adjust=False).mean()

    histogram = macd - signal

    return macd, signal, histogram


def detect_patterns(data):

    data = data.copy()

    body = abs(data["Close"] - data["Open"])

    lower_shadow = (
        np.minimum(data["Open"], data["Close"])
        - data["Low"]
    )

    upper_shadow = (
        data["High"]
        - np.maximum(data["Open"], data["Close"])
    )

    data["Hammer"] = (
        (lower_shadow >= body * 2) &
        (upper_shadow <= body)
    )

    data["Inverted Hammer"] = (
        (upper_shadow >= body * 2) &
        (lower_shadow <= body)
    )

    return data


# =========================================================
# PLOTLY THEME
# =========================================================

def apply_chart_theme(fig, height=500):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#cbd5e1"),
       
