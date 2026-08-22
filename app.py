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

        # יצירת מבנה נקי לגרף ולנפח
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_heights=[0.8, 0.2]
        )

        # נרות יפניים
        fig.add_trace(go.Candlestick(
            x=df['Date'], open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], showlegend=False,
            increasing_line_color='#00897b', decreasing_line_color='#e53935'
        ), row=1, col=1)

        # נפח מסחר
        colors = ['#00897b' if row['Close'] >= row['Open'] else '#e53935' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(
            x=df['Date'], y=df['Volume'], showlegend=False,
            marker_color=colors
        ), row=2, col=1)

        # הצמדת צירים לימין ללא שגיאות תחביר
        fig.update_yaxes(side="right", row=1, col=1, automargin=True)
        fig.update_yaxes(side="right", row=2, col=1, automargin=True)

        # נעילת ציר המחירים ופתיחת ציר הזמן לגרירה חלקה
        fig.update_yaxes(fixedrange=True)
        fig.update_xaxes(fixedrange=False)

        # עיצוב לבן נקי מקצה לקצה
        fig.update_layout(
            template='plotly_white',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            xaxis_rangeslider_visible=False,
            dragmode='pan',
            height=380,
            margin=dict(l=0, r=2, t=5, b=5)
        )

        config_options = {
            'displayModeBar': False,
            'scrollZoom': False,
            'doubleClick': 'reset'
        }

        st.plotly_chart(fig, use_container_width=True, config=config_options)

        # --- ניתוח טכני מעמיק, לימודי ומקצועי ---
        st.markdown("---")
        st.markdown("### 🎓 ניתוח מקצועי ועמוק של הגרף (למתחילים ולמתקדמים)")

        if timeframe == "חודש אחרון":
            st.markdown("""
            **מה רואים בטווח של חודש אחרון? (מיקוד על פסיכולוגיית המסחר בטווח הקצר)**
            * **המבנה הבסיסי למתחילים:** כל "נר" בגרף מייצג סיפור של יום מסחר שלם. נר ירוק אומר שהמחיר סיים גבוה מכפי שהתחיל (הקונים ניצחו היום), ונר אדום אומר שהמחיר סיים נמוך מכפי שהתחיל (המוכרים ניצחו). הפתילים (הקווים הדקים שיוצאים מהנר) מראים את שיא הגובה והשפל שאליהם הגיע המחיר במהלך אותו יום לפני שנסגר.
            * **מה קורה כרגע במגמה?** החודש האחרון מאופיין בתנועת **דשדוש (קונסולידציה)**. לאחר שהמניה הגיעה לאזורים גבוהים, הקצב נרגע. רואים נרות קטנים יחסית שמעידים על "דריכה במקום" והמתנה של השוק לחדשות או לטריגר הבא.
            * **ניתוח עומק של נפח המסחר (העמודות למטה):** שים לב לעמודות הנפח בתחתית הגרף. בימים האדומים (שבהם המחיר ירד), העמודות קצרות ונמוכות משמעותית בהשוואה לימים הירוקים. מבחינה מקצועית, זה סימן מעודד מאוד: המשמעות هي שאין פאניקה בשוק ואין גופים גדולים שמוכרים בהיסטריה. הירידות הקלות הן תוצאה של מימושי רווח טבעיים של סוחרים קטנים, ולא בריחה המונית של כסף חכם.
            """)
        elif timeframe == "3 חודשים":
            st.markdown("""
            **מה רואים בטווח של 3 חודשים? (ניתוח מגמה בינונית וזיהוי כיוון השוק)**
            * **המבנה הבסיסי למתחילים:** בטווח של שלושה חודשים אנחנו מקבלים "מבט-על" רחב יותר שמאפשר לזהות את הכיוון הכללי של המניה (האם היא עולה, יורדת או דורכת במקום).
            * **מה קורה כרגע במגמה?** רואים בבירור **גל עליות (מגמה שורית)**. המניה מייצרת מבנה שבו כל פסגה גבוהה יותר מהקודמת, וכל שפל גבוה מהשפל הקודם. המשמעות היא שהביקוש למניה גבוה מההיצע לאורך זמן.
            * **ניתוח עומק ופסיכולוגיית משקיעים:** רצף הנרות הירוקים הארוכים בשלבים המוקדמים של התקופה מלמד על כניסה של כסף מוסדי (גופים גדולים כמו קרנות פנסיה או בתי השקעות) שדוחפים את המחיר כלפי מעלה בעוצמה. האזורי תמיכה שמהם החל הזינוק מתפקדים כעת כרנות קשיחות שבהן הקונים חוזרים לקנות אוטומטית.
            """)
        elif timeframe == "שנה אחרונה":
            st.markdown("""
            **מה רואים בטווח של שנה אחרונה? (ניתוח מאקרו-טכני ומחזוריות ארוכת טווח)**
            * **המבנה הבסיסי למתחילים:** גרף שנתי מציג את כל המחזוריות הכלכלית שהחברה עברה – כולל תקופות משבר, דוחות רבעוניים מוצלחים, וגלי אופטימיות או פסימיות של הציבור הרחב.
            * **מה קורה כרגע במגמה?** הגרף חושף את נקודות המפנה המרכזיות בשנה החולפת. ניתן לראות כיצד המניה נחלשה בתקופות מסוימות אך ידעה לבנות את עצמה מחדש, לפרוץ רמות התנגדות קשות, ולייצר תשואה מצטברת מרשימה.
            * **ניתוח עומק מוסדי:** בטווח כזה, נפחי המסחר הגבוהים המלווים בנרות ארוכים מסמנים את האירועים הכלכליים המשמעותיים ביותר שבהם השוק קבע מחדש את שוויה הכלכלי האמיתי של החברה.
            """)
        else:
            st.markdown("""
            **מה רואים בכל ההיסטוריה? (פרספקטיבה היסטורית מלאה)**
            * **המבנה הבסיסי למתחילים:** מבט-על רב-שנתי שמראה לאן המניה הגיעה מרגע שהונפקה או החלה להיסחר ועד היום.
            * **ניתוח עומק מרכזי:** הסתכלות על כל ההיסטוריה מאפשרת לזהות את "תקרות הזכוכית" ההיסטוריות של המניה ואת רמות השפל העמוקות ביותר שלה כדי להבין את טווח המחירים האמיתי שלה לאורך שנים.
            """)

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
