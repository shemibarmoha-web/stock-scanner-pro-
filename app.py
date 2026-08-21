import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת - גרף מסחר מקצועי")

# תפריט ניווט
analysis_page = st.sidebar.selectbox(
    "🧭 בחר מסך ניתוח:",
    [
        "🕯️ גרף נרות יפניים",
        "📈 ניתוח טכני",
        "💰 ניתוח פונדמנטלי"
    ]
)

st.divider()
stock_symbol = st.text_input("הקלד את סמל המניה:", value="דלק קבוצה")

if stock_symbol:
    st.header(f"📊 תוצאות עבור: {stock_symbol}")
    
    if "גרף נרות יפניים" in analysis_page:
        st.subheader("🕯️ גרף נרות יפניים ונפח מסחר")
        
        # נתונים לדוגמה
        df = pd.DataFrame({
            'Date': ['2026-08-17', '2026-08-18', '2026-08-19', '2026-08-20', '2026-08-21'],
            'Open': [83.5, 83.0, 84.2, 85.0, 85.5],
            'High': [85.0, 84.5, 86.5, 86.2, 86.8],
            'Low': [82.5, 82.0, 83.8, 84.8, 85.1],
            'Close': [83.0, 84.2, 86.15, 85.5, 86.5],
            'Volume': [30, 50, 85, 40, 70]
        })

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])

        fig.add_trace(go.Candlestick(
            x=df['Date'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='נרות',
            increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
        ), row=1, col=1)

        colors = ['#26a69a' if row['Close'] >= row['Open'] else '#ef5350' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='נפח', marker_color=colors), row=2, col=1)

        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=500,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    elif "ניתוח טכני" in analysis_page:
        st.subheader("📈 ממוצעים נעים")
        tech_data = pd.DataFrame(np.random.randn(10, 2) * 1.5 + 85, columns=['שער', 'ממוצע נע'])
        st.line_chart(tech_data)

    else:
        st.subheader("💰 פונדמנטלי ומכפילים")
        st.markdown("מכפיל רווח נוכחי: **11.2**")
        fund_data = pd.DataFrame({'NAV מוערך': [78, 82, 85, 91]})
        st.area_chart(fund_data)

else:
    st.info("אנא הזן שם מניה.")
