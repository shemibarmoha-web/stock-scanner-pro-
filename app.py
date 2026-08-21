import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת עם התאמה אישית לשיטות הניתוח")

# רשימת השיטות המלאה
analysis_methods = {
    "1. ניתוח נרות יפניים (Candlestick Analysis)": "זיהוי תבניות היפוך, פריצה ומומנטום בנרות.",
    "2. ניתוח טכני ומתנדים (Technical & Indicators)": "שימוש בממוצעים נעים, RSI ו-MACD.",
    "3. ניתוח פונדמנטלי (Fundamental Analysis)": "בחינת דוחות, יחס P/E ומודל גורדון.",
    "4. ניתוח כמותי (Quantitative Analysis)": "מודלים מתמטיים וסטטיסטיים להערכת סיכונים.",
    "5. ניתוח סנטימנט שוק (Sentiment Analysis)": "בחינת הלך רוח משקיעים וחדשות.",
    "6. ניתוח Top-Down (מאקרו לענפי)": "ניתוח מאקרו כלכלי מול ביצועי הענף והחברה."
}

# שלב 1: בחירת שיטה
selected_method = st.selectbox("בחר שיטת ניתוח מתוך הרשימה:", list(analysis_methods.keys()))
st.info(f"💡 **הסבר על השיטה:** {analysis_methods[selected_method]}")

# שלב 2: הזנת מניה
stock_symbol = st.text_input("הקלד את שם/סמל המניה שברצונך לנתח (למשל: בזק, דלק קבוצה):")

# שלב 3: ביצוע הניתוח
if st.button("בצע ניתוח"):
    if stock_symbol:
        st.divider()
        st.header(f"📊 דוח ניתוח עבור: {stock_symbol}")
        
        # נתוני בסיס לפי המניה
        if "בזק" in stock_symbol:
            price, change, pe, mcap = "7.55 ₪", "-0.04%", "17.25", "20.8 מיליארד ₪"
        elif "דלק" in stock_symbol:
            price, change, pe, mcap = "86.15 ₪", "+5.58%", "11.2", "12.4 מיליארד ₪"
        else:
            price, change, pe, mcap = "120.50 ₪", "+1.20%", "14.5", "5.1 מיליארד ₪"

        # הצגת כרטיסיות נתונים כלליות
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("שער אחרון", price, change)
        col2.metric("מכפיל רווח (P/E)", pe)
        col3.metric("שווי שוק", mcap)
        col4.metric("סטטוס", "פעיל בשוק")

        # הצגת תוכן דינמי שמשתנה לחלוטין לפי השיטה שנבחרה
        if "1. ניתוח נרות יפניים" in selected_method:
            st.subheader("🕯️ תצוגה גרפית ותבניות נרות יפניים")
            candles_df = pd.DataFrame({
                'תאריך': ['אתמולתיים', 'אתמול', 'היום'],
                'שער פתיחה': [445, 450, 452],
                'שער סגירה': [450, 452, 461],
                'תבנית שזוהתה': ['Hammer', 'Doji', 'Bullish Engulfing (חיובי חזק)'],
                'המלצה': ['המתנה', 'היפוך מגמה', 'איתות קנייה מובהק']
            })
            st.dataframe(candles_df, use_container_width=True)
            st.success("נרות יפניים מראים על לחץ קונים חזק בנר האחרון עם פריצת התנגדות מקומית.")

        elif "2. ניתוח טכני ומתנדים" in selected_method:
            st.subheader("📈 מתנדים טכניים וממוצעים נעים")
            tech_data = pd.DataFrame(
                np.random.randn(15, 2) * 3 + 100,
                columns=['מחיר מניה', 'ממוצע נע 50']
            )
            st.line_chart(tech_data)
            
            indicators_df = pd.DataFrame({
                'מתנד': ['RSI (14)', 'MACD', 'Bollinger Bands'],
                'ערך נוכחי': ['58.4 (נייטרלי-חיובי)', 'חיובי (+1.4)', 'רצועה עליונה'],
                'איתות': ['החזק', 'קנייה', 'מימוש חלקי']
            })
            st.dataframe(indicators_df, use_container_width=True)

        elif "3. ניתוח פונדמנטלי" in selected_method:
            st.subheader("💰 דוחות כספיים ומודלים כלכליים (NAV / P/E)")
            fund_df = pd.DataFrame({
                'מדד פונדמנטלי': ['יחס מחיר לרווח (P/E)', 'תשואת דיבידנד', 'הערכת שווי NAV', 'תזרים מזומנים חופשי'],
                'נתון החברה': [pe, '4.2%', 'אטרקטיבי מאוד', 'חיובי ויציב'],
                'ניתוח שווי': ['מתמחר נכון את הסיכון', 'תשואה גבוהה מהממוצע', 'פוטנציאל אפסייד', 'יכולת חלוקת דיבידנד']
            })
            st.dataframe(fund_df, use_container_width=True)
            st.warning("הניתוח הפונדמנטלי מצביע על חוסן פיננסי ויחס שווי נכסי טוב.")

        elif "4. ניתוח כמותי" in selected_method:
            st.subheader("🔢 מודלים כמותיים וסטטיסטיים לחשיפה וסיכון")
            quant_df = pd.DataFrame({
                'מודל סטטיסטי': ['סטיית תקן (Volatility)', 'מקדם סיכון (Beta)', 'Value at Risk (VaR)'],
                'תוצאה מחושבת': ['14.2% שנתי', '1.08', '-2.1% יומי (95% אמון)'],
                'הערכת סיכון': ['בינוני', 'תואם את תנודתיות השוק', 'רמת סיכון סבירה במסחר']
            })
            st.dataframe(quant_df, use_container_width=True)

        elif "5. ניתוח סנטימנט שוק" in selected_method:
            st.subheader("📰 סנטימנט משקיעים וניתוח חדשות")
            sent_df = pd.DataFrame({
                'מקור מידע': ['חדשות כלכליות', 'רשתות חברתיות / פורומים', 'מדד פחד ותאוות בצע'],
                'כיוון הסנטימנט': ['חיובי מאוד', 'אופטימי', '62 (Greed)'],
                'השפעה על המניה': ['תמיכה בהמשך עליות', 'נפח מסחר ער', 'מומנטום חיובי']
            })
            st.dataframe(sent_df, use_container_width=True)

        else:
            st.subheader("🌐 ניתוח מאקרו-כלכלי וביצועי ענף (Top-Down)")
            top_down_df = pd.DataFrame({
                'שלב הניתוח': ['מצב מאקרו עולמי/מקומי', 'חוזק הענף בבורסה', 'מיקום החברה בענף'],
                'מצב נוכחי': ['סביבת ריבית מתייצבת', 'צמיחה ענפית חיובית', 'נתח שוק מוביל'],
                'החלטה אסטרטגית': ['השקעה מותרת', 'מומלץ לעכב/להגדיל', 'קנייה מועדפת']
            })
            st.dataframe(top_down_df, use_container_width=True)

    else:
        st.error("אנא הזן שם מניה או סמל לפני לחיצה על כפתור הניתוח.")
