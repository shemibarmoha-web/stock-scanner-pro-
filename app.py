import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת - גרף מסחר מקצועי")

# תפריט ניווט ראשי
analysis_page = st.selectbox(
    "🧭 בחר מסך ניתוח:",
    [
        "🕯️ 1. גרף נרות יפניים (Candlestick & Volume)",
        "📈 2. ניתוח טכני ומתנדים",
        "💰 3. ניתוח פונדמנטלי",
        "🔢 4. ניתוח כמותי",
        "📰 5. ניתוח סנטימנט שוק",
        "🌐 6. ניתוח Top-Down (מאקרו)"
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

    # הצגת גרף נרות יפניים אמיתי בסגנון TradingView
    if "גרף נרות יפניים" in analysis_page:
        st.subheader("🕯️ גרף נרות יפניים ונפח מסחר (TradingView Style)")
        st.write("גרף מקצועי הכולל גופים, פתילות (Wicks), צבעי עולים ויורדים וגרף נפח מסחר תחתון:")
        
        # נתוני סימולציה נרחבים לבניית נרות ופתילות
        df = pd.DataFrame({
            'Date': ['2026-08-13', '2026-08-14', '2026-08-17', '2026-08-18', '2026-08-19', '2026-08-20', '2026-08-21'],
            'Open': [80.0, 82.0, 83.5, 83.0, 84.2, 85.0, 85.5],
            'High': [83.0, 84.0, 85.0, 84.5, 86.5, 86.2, 86.8],
            'Low': [79.5, 81.5, 82.5, 82.0, 83.8, 84.8, 85.1],
            'Close': [82.0, 83.5, 83.0, 84.2, 86.15, 85.5, 86.5],
            'Volume': [45, 60, 30, 50, 85, 40, 70]
        })

        # יצירת גרף משולב (נרות למעלה, נפח מסחר למטה)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, row_heights=[0.7, 0.3])

        # הוספת נרות יפניים (Candlestick)
        fig.add_trace(go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='נרות יפניים',
            increasing_line_color='#26a69a', increasing_fillcolor='#26a69a',  # ירוק
            decreasing_line_color='#ef5350', decreasing_fillcolor='#ef5350'   # אדום
        ), row=1, col=1)

        # הוספת גרף נפח המסחר (Volume Bars) למטה בצבעים תואמים
        colors = ['#26a69a' if row['Close'] >= row['Open'] else '#ef5350' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(
            x=df['Date'], y=df['Volume'], name='נפח מסחר (Volume)',
            marker_color=colors
        ), row=2, col=1)

        # עיצוב מראה הגרף בסגנון כהה ומקצועי
        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=600,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success("""
        ### 💡 תובנות טכניות מהגרף:
        * **גופים ופתילות:** הנרות הירוקים מראים שליטת קונים, והפתילות הארוכות משקפות את טווח המחירים התוך-יומי.
        * **נפח מסחר (Volume):** העמודות הגבוהות בתחתית הגרף מעידות על הזרמת הון ערה ואישור לפריצת רמות ההתנגדות.
        """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 ממוצעים נעים ומתנדים (RSI / MACD)")
        tech_data = pd.DataFrame(np.random.randn(10, 2) * 1.5 + 85, columns=['שער בפועל', 'ממוצע נע 20'])
        st.line_chart(tech_data)
        st.info("מדד RSI עומד על 58.4 (אזור חיובי בריא).")

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 שווי נקי נכסי ותשואות (NAV)")
        fund_data = pd.DataFrame({'NAV מוערך': [78, 82, 85, 91]})
        st.area_chart(fund_data)
        st.markdown(f"מכפיל הרווח עומד על **{pe}**.")

    elif "כמותי" in analysis_page:
        st.subheader("🔢 תנודתיות וסיכון")
        quant_data = pd.DataFrame({'תנודתיות יומית (%)': [1.1, 1.4, 0.8, 1.3]})
        st.bar_chart(quant_data)

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 סנטימנט משקיעים")
        sent_data = pd.DataFrame({'מדד גריד': [50, 54, 59, 62]})
        st.line_chart(sent_data)

    else:
        st.subheader("🌐 סביבת מאקרו וענף")
        macro_data = pd.DataFrame({'מדד סקטוריאלי': [180, 185, 192, 198]})
        st.area_chart(macro_data)

else:
    st.info("אנא הזן שם מניה.")
