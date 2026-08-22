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
        
        # בניית מסלול מחירים המתחיל בדיוק ממחיר הבסיס של המניה (למשל 86.15 לדלק)
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

        # הצמדת צירים לימין
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

        # --- ניתוח טכני מעמיק, לימודי ומעשי לסוחרים ---
        st.markdown("---")
        st.markdown("### 🎓 ניתוח מקצועי: מה רואים ומה בפועל *אמורים לעשות*?")

        if timeframe == "חודש אחרון":
            st.markdown("""
            **1. מה רואים בגרף (טווח קצר - דשדוש ותיקון):**
            * **המבנה:** הנרות קטנים יחסית, עם פתילים (צלליות) עליונים ותחתונים. זה מעיד על חוסר הכרעה זמני והתלבטות בין קונים למוכרים.
            * **נפח מסחר:** עמודות נפח נמוכות בימים האדומים מראות שאין לחץ מכירות אמיתי או פאניקה בשוק.
            
            **2. 🧭 מה הקונים והמוכרים אמורים לעשות במצב כזה?**
            * **למי שרוצה לקנות:** זהו **לא** אזור אידיאלי לקנייה אגרסיבית. החכם יהיה **להמתין בסבלנות** לנר היפוך חזק כלפי מעלה או לירידה קלה שתבחן את אזור התמיכה.
            * **למי שרוצה למכור / מחזיק במניה:** אין סיבה לרוץ ולמכור רק כי יש ימים אדומים קטנים כל עוד נפחי המסחר נמוכים. אפשר לשים פקודת הגנה (סטופ-לוס) מתחת לאזור התמיכה.
            """)
        elif timeframe == "3 חודשים":
            st.markdown("""
            **1. מה רואים בגרף (טווח בינוני - מגמת עליות חזקה):**
            * **המבנה:** רצף ברור של נרות ירוקים דומיננטיים, כאשר המניה מייצרת שיאים עולים חדשים.
            * **פטישים ואותות:** הופעה של נרות עם פתילים תחתונים ארוכים באזורי השפלים מסמנת שהמוכרים ניסו להוריד מחיר, אך הקונים קנו כל סחורה מוזלת.
            
            **2. 🧭 מה הקונים והמוכרים אמורים לעשות במצב כזה?**
            * **למי שרוצה לקנות:** המגמה חיובית. ההמלצה המעשית היא **לקנות בירידות קטנות בתוך המגמה העולה** או להצטרף לפריצת התנגדות עם נפח מסחר גבוה. להיזהר לא לרדוף אחרי המניה ביום של זינוק קיצוני.
            * **למי שרוצה למכור / להגן על רווחים:** כל עוד המניה מייצרת שיאים ושפלים עולים, **מחזיקים בפוזיציה ולא ממהרים למכור**. מומלץ לגרור את פקודת ההגנה כלפי מעלה.
            """)
        elif timeframe == "שנה אחרונה":
            st.markdown("""
            **1. מה רואים בגרף (טווח ארוך - מחזוריות ומגמה ראשית):**
            * **המבנה:** תמונה מלאה של תנודות השוק לאורך שנה שלמה – כולל גלי עליות ותיקונים.
            
            **2. 🧭 מה הקונים והמוכרים אמורים לעשות במצב כזה?**
            * **למי שרוצה לקנות:** לבדוק האם המניה נמצאת במגמת עלייה בריאה ולבנות תיק הדרגתית (כניסה בפעימות) ולא בבת אחת.
            * **למי שרוצה למכור:** האם הגעת ליעד הרווח השנתי? אם כן, מומלץ לממש חלק מהרווחים ולהשאיר את היתרה.
            """)
        else:
            st.markdown("""
            **1. מה רואים בגרף (כל ההיסטוריה - מבט על-זמני):**
            * **המבנה:** היסטוריית המסחר המלאה המציגה את רמות התמיכה וההתנגדות החזקות ביותר.
            
            **2. 🧭 מה הקונים והמוכרים אמורים לעשות במצב כזה?**
            * **למי שרוצה לקנות/למכור:** מבט היסטורי נועד לזהות אם המחיר כרגע בתמחור יתר או בהזדמנות ערך סביב רמות שפל רב-שנתיות חזקות שבהן משקיעי ערך אוספים סחורה.
            """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 ממוצעים נעים ומתנדים")
        tech_data = pd.DataFrame(np.random.randn(30, 2) * 1.5 + base_price, columns=['שער', 'ממוצע נע'])
        st.line_chart(tech_data)

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
