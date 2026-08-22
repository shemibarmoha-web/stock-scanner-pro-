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
            horizontal=True,
            key="tf_candlestick"
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
        st.markdown("### 🎓 מה לראות ומה לעשות בגרף?")
        st.markdown("""
        * **לקנייה:** המתן שהמחיר יירד ויקבל תמיכה, או יפרוץ התנגדות כלפי מעלה.
        * **למכירה:** הגדר סטופ-לוס או נקודת יציאה אם המחיר שובר תמיכה חשובה.
        """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 מגמת שער וממוצעים נעוצים (MA 7 ו-MA 20)")
        
        timeframe_tech = st.radio(
            "בחר טווח זמן להצגה:",
            ["חודש אחרון", "3 חודשים", "שנה אחרונה", "כל ההיסטוריה"],
            horizontal=True,
            key="tf_tech"
        )

        np.random.seed(100)
        dates_tech = pd.date_range(start="2021-01-01", end="2026-08-22", freq="B")
        n_tech = len(dates_tech)
        returns_tech = np.random.normal(0.0002, 0.015, n_tech)
        price_path_tech = base_price * np.cumprod(1 + returns_tech)
        
        tech_df = pd.DataFrame({
            'Date': dates_tech,
            'Price': price_path_tech,
            'MA7': pd.Series(price_path_tech).rolling(window=7).mean().fillna(base_price),
            'MA20': pd.Series(price_path_tech).rolling(window=20).mean().fillna(base_price)
        })

        if timeframe_tech == "חודש אחרון":
            tech_df = tech_df.tail(22)
        elif timeframe_tech == "3 חודשים":
            tech_df = tech_df.tail(66)
        elif timeframe_tech == "שנה אחרונה":
            tech_df = tech_df.tail(250)

        fig_tech = go.Figure()

        # קו המחיר
        fig_tech.add_trace(go.Scatter(
            x=tech_df['Date'], y=tech_df['Price'],
            mode='lines', name='שער מניה',
            line=dict(color='#1e88e5', width=2.5)
        ))

        # ממוצע נע מהיר (7 ימים)
        fig_tech.add_trace(go.Scatter(
            x=tech_df['Date'], y=tech_df['MA7'],
            mode='lines', name='ממוצע נע מהיר (7 ימים)',
            line=dict(color='#00897b', width=2)
        ))

        # ממוצע נע קצר (20 ימים)
        fig_tech.add_trace(go.Scatter(
            x=tech_df['Date'], y=tech_df['MA20'],
            mode='lines', name='ממוצע נע קצר (20 ימים)',
            line=dict(color='#fb8c00', width=2, dash='dash')
        ))

        fig_tech.update_layout(
            template='plotly_white',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            xaxis_rangeslider_visible=False,
            dragmode='pan',
            height=380,
            margin=dict(l=0, r=2, t=5, b=5),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(side="right")
        )
        
        fig_tech.update_xaxes(fixedrange=False, range=[tech_df['Date'].iloc[0], tech_df['Date'].iloc[-1]])
        fig_tech.update_yaxes(fixedrange=True)

        st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False, 'doubleClick': 'reset'})

        # --- הסבר מקצועי, מדויק וברור לפעולה ---
        st.markdown("---")
        st.markdown("### 🎓 מדריך מקצועי: ניתוח מגמה באמצעות ממוצעים נעוצים (MA 7 ו-MA 20)")
        st.markdown("""
        כדי לנתח נכון את התנהגות המניה בעזרת הגרף, יש להכיר את תפקידם המדויק של הקווים ולפעול לפיהם:

        #### 1. פיענוח הרכיבים בגרף:
        * **שער המניה (קו כחול):** מציג את המחיר בפועל שבו נסחרת המניה בכל יום נתון.
        * **ממוצע נע מהיר (MA 7 - קו ירוק):** מחושב לפי ממוצע השערים של **7 ימי המסחר האחרונים**. מכיוון שהוא קצר-טווח מאוד, הוא מגיב מהר מאוד לכל תנודה חדה בשוק ומצביע על המומנטום המיידי.
        * **ממוצע נע קצר (MA 20 - קו כתום מקוטע):** מחושב לפי ממוצע השערים של **20 ימי המסחר האחרונים** (כחודש מסחר מלא). הוא מייצג את המגמה העוקבת ומסנן רעשים קצרי טווח.

        #### 2. 🧭 כללי עבודה למסחר ולניהול סיכונים:
        * **איתות לכיוון חיובי (מומנטום עולה):** 
          * כאשר קו המחיר (הכחול) והממוצע המהיר (הירוק) נמצאים **מעל** הממוצע הקצר (הכתום), המגמה הראשית היא חיובית.
          * **נקודת כניסה אידיאלית (איסוף):** סוחרים ממתינים לזמן שבו המניה עושה "תיקון" בריא ויורדת לבחון את אזור התמיכה של הממוצע המהיר (הירוק). אם המחיר נבלם שם ועושה סימן חזרה כלפי מעלה, זו נקודת כניסה מועדפת.
        * **איתות אזהרה וניהול סיכונים (הגנה על התיק):**
          * כאשר הממוצע המהיר (הירוק) יורד וחוצה את הממוצע הקצר (הכתום) **כלפי מטה**, או לחלופין כשהמחיר נופל וסוגר מתחת לשניהם – השוק מאבד את מומנטום הקונים.
          * במצב כזה, ההתנהלות המקצועית דורשת הפעלת זהירות, מימוש חלק מהרווחים או הגדרת פקודת סטופ-לוס (עצירת הפסד) כדי להימנע מחשיפה לירידות עמוקות יותר.
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
