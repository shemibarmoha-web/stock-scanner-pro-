import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת")

# תפריט ניווט ראשי
analysis_page = st.selectbox(
    "🧭 בחר מסך ניתוח:",
    [
        "🕯️ 1. גרף נרות יפניים (Candlestick & Volume)",
        "📈 2. ניתוח טכני ומתנדים",
        "💰 3. ניתוח פונדמנטלי (NAV ושווי)",
        "🔢 4. ניתוח כמותי ותנודתיות",
        "📰 5. סנטימנט שוק",
        "🌐 6. מאקרו וענף"
    ]
)

st.divider()

stock_symbol = st.text_input("הקלד את סמל המניה:", value="דלק קבוצה")

if stock_symbol:
    st.header(f"📊 תוצאות עבור: {stock_symbol}")
    
    if "בזק" in stock_symbol:
        price, change, pe, mcap = "7.55 ₪", "-0.04%", "17.25", "20.8 מיליארד ₪"
    elif "דלק" in stock_symbol:
        price, change, pe, mcap = "86.15 ₪", "+5.58%", "11.2", "12.4 מיליארד ₪"
    else:
        price, change, pe, mcap = "120.50 ₪", "+1.20%", "14.5", "5.1 מיליארד ₪"

    col1, col2, col3 = st.columns(3)
    col1.metric("שער אחרון", price, change)
    col2.metric("מכפיל רווח", pe)
    col3.metric("שווי שוק", mcap)

    st.divider()

    if "גרף נרות יפניים" in analysis_page:
        st.subheader("🕯️ גרף נרות יפניים ונפח מסחר")
        
        timeframe = st.radio(
            "בחר טווח זמן להצגה:",
            ["חודש אחרון", "3 חודשים", "שנה אחרונה", "כל ההיסטוריה"],
            horizontal=True
        )

        np.random.seed(42)
        dates = pd.date_range(start="2021-01-01", end="2026-08-22", freq="B")
        n = len(dates)
        returns = np.random.normal(0.0003, 0.018, n)
        price_path = 100 * np.cumprod(1 + returns)
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': price_path * (1 + np.random.uniform(-0.008, 0.008, n)),
            'High': price_path * (1 + np.random.uniform(0.003, 0.02, n)),
            'Low': price_path * (1 - np.random.uniform(0.003, 0.02, n)),
            'Close': price_path,
            'Volume': np.random.randint(30, 200, n)
        })

        if timeframe == "חודש אחרון":
            df = df.tail(22)
        elif timeframe == "3 חודשים":
            df = df.tail(66)
        elif timeframe == "שנה אחרונה":
            df = df.tail(250)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.02, row_heights=[0.8, 0.2])

        # נרות יפניים
        fig.add_trace(go.Candlestick(
            x=df['Date'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], showlegend=False,
            increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
        ), row=1, col=1)

        # נפח מסחר
        colors = ['#26a69a' if row['Close'] >= row['Open'] else '#ef5350' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(
            x=df['Date'], y=df['Volume'], showlegend=False,
            marker_color=colors
        ), row=2, col=1)

        # ציר מחירים מימין - נעילת ציר ה-Y כך שלא יברח למעלה או למטה
        fig.update_yaxes(side="right", row=1, col=1, automargin=True)
        fig.update_yaxes(side="right", row=2, col=1, automargin=True)

        # נעילת תנועת ציר ה-Y כך שהגרירה תהיה אך ורק על ציר הזמן (X) והמחירים יישארו במקום
        fig.update_xaxes(fixedrange=False)
        fig.update_yaxes(fixedrange=True)

        # הגדרת פריסה נקייה
        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=380,
            margin=dict(l=0, r=2, t=5, b=5)
        )

        config_options = {
            'displayModeBar': False,
            'scrollZoom': True,
            'doubleClick': 'reset'
        }

        st.plotly_chart(fig, use_container_width=True, config=config_options)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 ממוצעים נעים ומתנדים")
        tech_data = pd.DataFrame(np.random.randn(30, 2) * 1.5 + 85, columns=['שער', 'ממוצע נע'])
        st.line_chart(tech_data)

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 שווי נקי נכסי ותשואות (NAV)")
        fund_data = pd.DataFrame({'NAV מוערך': [78, 82, 85, 91, 95]})
        st.area_chart(fund_data)

    elif "כמותי" in analysis_page:
        st.subheader("🔢 תנודתיות וסיכון")
        quant_data = pd.DataFrame({'תנודתיות': [1.1, 1.4, 0.8, 1.3, 1.0]})
        st.bar_chart(quant_data)

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 סנטימנט משקיעים")
        sent_data = pd.DataFrame({'סנטימנט': [50, 54, 59, 62, 65]})
        st.line_chart(sent_data)

    else:
        st.subheader("🌐 סביבת מאקרו וענף")
        macro_data = pd.DataFrame({'מדד סקטוריאלי': [180, 185, 192, 198, 205]})
        st.area_chart(macro_data)

else:
    st.info("אנא הזן שם מניה.")
