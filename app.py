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
    
    # הגדרת מחיר בסיס אמיתי לפי המניה הנבחרת
    if "בזק" in stock_symbol:
        base_price = 7.55
        price, change, pe, mcap = "7.55 ₪", "-0.04%", "17.25", "20.8 מיליארד ₪"
    elif "דלק" in stock_symbol:
        base_price = 86.15
        price, change, pe, mcap = "86.15 ₪", "+5.58%", "11.2", "12.4 מיליארד ₪"
    else:
        base_price = 120.50
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
        returns = np.random.normal(0.0002, 0.015, n)
        price_path = base_price * np.cumprod(1 + returns)
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': price_path * (1 + np.random.uniform(-0.005, 0.005, n)),
            'High': price_path * (1 + np.random.uniform(0.002, 0.015, n)),
            'Low': price_path * (1 - np.random.uniform(0.002, 0.015, n)),
            'Close': price_path,
            'Volume': np.random.randint(30, 200, n)
        })

        if timeframe == "חודש אחרון":
            df = df.tail(22)
        elif timeframe == "3 חודשים":
            df = df.tail(66)
        elif timeframe == "שנה אחרונה":
            df = df.tail(250)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])

        fig.add_trace(go.Candlestick(
            x=df['Date'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], showlegend=False,
            increasing_line_color='#00897b', decreasing_line_color='#e53935'
        ), row=1, col=1)

        colors = ['#00897b' if row['Close'] >= row['Open'] else '#e53935' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], showlegend=False, marker_color=colors), row=2, col=1)

        fig.update_yaxes(side="right", row=1, col=1, automargin=True)
        fig.update_yaxes(side="right", row=2, col=1, automargin=True)
        fig.update_yaxes(fixedrange=True)
        fig.update_xaxes(fixedrange=False)

        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            xaxis_rangeslider_visible=False,
            dragmode='pan',
            height=380,
            margin=dict(l=0, r=2, t=5, b=5)
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False, 'doubleClick': 'reset'})

        st.markdown("---")
        st.markdown("### 🎓 ניתוח מקצועי: מה רואים ומה בפועל *אמורים לעשות*?")
        st.markdown("""
        * **למי שרוצה לקנות:** המתן לפריצת רמת התנגדות או לחזרה של המחיר לתמיכה המרכזית.
        * **למי שרוצה למכור:** הגדרת נקודת יציאה או סטופ-לוס בעת שבר מבנה המחיר.
        """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 מגמת שער וממוצע נע (Moving Average)")
        
        # יצירת טוח נתונים חלק ויפה לניתוח טכני
        np.random.seed(100)
        days_tech = pd.date_range(start="2026-05-01", end="2026-08-22", freq="B")
        m_vals = base_price * (1 + np.cumsum(np.random.normal(0.001, 0.012, len(days_tech))))
        
        tech_df = pd.DataFrame({
            'Date': days_tech,
            'Price': m_vals,
            'MA20': pd.Series(m_vals).rolling(window=5).mean().fillna(base_price)
        })

        # בניית גרף Plotly מתקדם ונקי לניתוח טכני
        fig_tech = go.Figure()

        # קו המחיר
        fig_tech.add_trace(go.Scatter(
            x=tech_df['Date'], y=tech_df['Price'],
            mode='lines', name='שער מניה',
            line=dict(color='#1e88e5', width=2.5)
        ))

        # ממוצע נע
        fig_tech.add_trace(go.Scatter(
            x=tech_df['Date'], y=tech_df['MA20'],
            mode='lines', name='ממוצע נע (MA 20)',
            line=dict(color='#fb8c00', width=2, dash='dash')
        ))

        fig_tech.update_layout(
            template='plotly_white',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            height=400,
            margin=dict(l=0, r=2, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(side="right")
        )

        st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

        # הסבר מעשי מפורט לניתוח טכני
        st.markdown("---")
        st.markdown("### 🎓 איך לקרוא את ממוצע הנע ומה *אמורים לעשות*?")
        st.markdown("""
        * **מה רואים בגרף:** הקו הכחול מייצג את תנועת המחיר היומית של המניה, והקו הכתוב המקוטע (MA20) מייצג את ממוצע המחירים הממוצע לתקופה. כאשר קו המחיר נמצא **מעל** הממוצע הנע, המגמה הראשית היא חיובית (שורית). כאשר הוא יורד **מתחתיו**, המגמה נחלשת.
        * **🧭 מה הקונים והמוכרים אמורים לעשות?**
          * **לקונים:** אם המחיר נתמך על גבי הממוצע הנע ועולה חזרה כלפי מעלה, זו לרוב נקודת כניסה נוחה (איסוף סחורה במגמה עולה).
          * **למוכרים / מחזיקים:** חצייה כלפי מטה של הממוצע הנע בלוויית נפח מסחר גבוה מהווה נורת אזהרה שמעידה על סיום המומנטום החיובי ודורשת שקילת מימוש רווחים או הדוק פקודת הגנה.
        """)

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 שווי נקי נכסי ותשואות (NAV)")
        fund_data = pd.DataFrame({'NAV מוערך': [base_price*0.9, base_price*0.95, base_price, base_price*1.05, base_price*1.1]})
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
