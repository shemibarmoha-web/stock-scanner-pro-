import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת - גרף מסחר היסטורי")

# תפריט ניווט ראשי
analysis_page = st.selectbox(
    "🧭 בחר מסך ניתוח:",
    [
        "🕯️ 1. גרף נרות יפניים (Candlestick & Volume)",
        "📈 2. ניתוח טכני ומתנדים",
        "💰 3. ניתוח פונדמנטלי (NAV ושווי)",
        "🔢 4. ניתוח כמותי ותנודתיות",
        "📰 5. ניתוח סנטימנט שוק",
        "🌐 6. ניתוח מאקרו וענף (Top-Down)"
    ]
)

st.divider()

# הזנת מניה
stock_symbol = st.text_input("הקלד את סמל המניה:", value="דלק קבוצה")

if stock_symbol:
    st.header(f"📊 תוצאות עבור: {stock_symbol}")
    
    # נתונים בסיסיים
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

    # הצגת הדפים לפי בחירת המשתמש
    if "גרף נרות יפניים" in analysis_page:
        st.subheader("🕯️ גרף נרות יפניים היסטורי עם ציר זמן (TradingView Style)")
        st.write("השתמש בסרגל הזמן התחתון או לגרור את הגרף כדי לצפות בתנועת המחירים לאורך זמן:")
        
        # יצירת סימולציית נתונים היסטורית רחבה (לאורך חודשים רבים)
        np.random.seed(42)
        dates = pd.date_range(start="2025-01-01", end="2026-08-21", freq="B") # ימי מסחר
        n = len(dates)
        
        # בניית מסלול מחירים סימולציוני ריאליסטי
        returns = np.random.normal(0.0005, 0.02, n)
        price_path = 100 * np.cumprod(1 + returns)
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': price_path * (1 + np.random.uniform(-0.01, 0.01, n)),
            'High': price_path * (1 + np.random.uniform(0.005, 0.025, n)),
            'Low': price_path * (1 - np.random.uniform(0.005, 0.025, n)),
            'Close': price_path,
            'Volume': np.random.randint(20, 150, n)
        })

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # הוספת נרות יפניים
        fig.add_trace(go.Candlestick(
            x=df['Date'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='נרות יפניים',
            increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
        ), row=1, col=1)

        # הוספת נפח מסחר
        colors = ['#26a69a' if row['Close'] >= row['Open'] else '#ef5350' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(
            x=df['Date'], y=df['Volume'], name='נפח מסחר (Volume)',
            marker_color=colors
        ), row=2, col=1)

        # הפעלת ציר הזמן והסליידר ההיסטורי
        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=True,  # מציג את סרגל הזמן בתחתית הגרף
            height=650,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis2_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)
        st.success("💡 **טיפ:** ניתן לגרור את הידיות בסרגל התחתון כדי להתמקד בתקופות זמן ספציפיות או להרחיב את המבט לאחור.")

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 ממוצעים נעים ומתנדים (RSI / MACD)")
        tech_data = pd.DataFrame(np.random.randn(30, 2) * 1.5 + 85, columns=['שער בפועל', 'ממוצע נע 20'])
        st.line_chart(tech_data)
        st.info("מדד RSI עומד על 58.4 – מצביע על מומנטום חיובי בריא.")

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 שווי נקי נכסי ותשואות (NAV)")
        fund_data = pd.DataFrame({'NAV מוערך': [78, 82, 85, 91, 95]})
        st.area_chart(fund_data)
        st.markdown(f"מכפיל הרווח הנוכחי עומד על **{pe}**.")

    elif "כמותי" in analysis_page:
        st.subheader("🔢 תנודתיות וסיכון")
        quant_data = pd.DataFrame({'תנודתיות יומית (%)': [1.1, 1.4, 0.8, 1.3, 1.0]})
        st.bar_chart(quant_data)

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 סנטימנט משקיעים ברשתות")
        sent_data = pd.DataFrame({'מדד סנטימנט': [50, 54, 59, 62, 65]})
        st.line_chart(sent_data)

    else:
        st.subheader("🌐 סביבת מאקרו וענף (Top-Down)")
        macro_data = pd.DataFrame({'מדד סקטוריאלי': [180, 185, 192, 198, 205]})
        st.area_chart(macro_data)

else:
    st.info("אנא הזן שם מניה.")
