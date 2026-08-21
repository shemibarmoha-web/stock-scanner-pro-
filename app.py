import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות ונתונים פיננסיים מתקדמת")

# הגדרת רשימת השיטות
analysis_methods = {
    "1. ניתוח טכני (Technical Analysis)": "שימוש בנרות יפניים, מתנדים ומגמות מחיר.",
    "2. ניתוח פונדמנטלי (Fundamental Analysis)": "בחינת דוחות, יחס P/E ומודל גורדון.",
    "3. ניתוח כמותי (Quantitative Analysis)": "מודלים מתמטיים וסטטיסטיים להערכת סיכונים.",
    "4. ניתוח סנטימנט שוק (Sentiment Analysis)": "בחינת הלך רוח משקיעים וחדשות.",
    "5. ניתוח Top-Down (מאקרו לענפי)": "ניתוח מאקרו כלכלי מול ביצועי הענף והחברה."
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
        st.header(f"📊 דוח ניתוח ונתוני שוק עבור: {stock_symbol}")
        
        # התאמת נתונים לדוגמה בהתאם למניה שהוקלדה
        if "בזק" in stock_symbol:
            price, change, pe, mcap = "7.55 ₪", "-0.04%", "17.25", "20.8 מיליארד ₪"
        elif "דלק" in stock_symbol:
            price, change, pe, mcap = "86.15 ₪", "+5.58%", "11.2", "12.4 מיליארד ₪"
        else:
            price, change, pe, mcap = "120.50 ₪", "+1.20%", "14.5", "5.1 מיליארד ₪"

        # הצגת מדדים מובילים
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("שער אחרון", price, change)
        col2.metric("מכפיל רווח (P/E)", pe)
        col3.metric("שווי שוק", mcap)
        col4.metric("מגמת מסחר", "חיובית 📈", "פעיל")

        # גרף ויזואלי
        st.subheader("📈 גרף תנועת שערים תקופתי")
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) * 2 + 100,
            columns=['שער סגירה', 'ממוצע נע']
        )
        st.line_chart(chart_data)

        # הצגת טבלת נתונים מפורטת לפי השיטה שנבחרה
        st.subheader("📋 ממצאים וניתוח נתונים מורחב")
        if "1. ניתוח טכני" in selected_method:
            details_df = pd.DataFrame({
                'אינדיקטור טכני': ['RSI (14)', 'MACD', 'רמת תמיכה', 'רמת התנגדות'],
                'ערך מדגם': ['56.4 (נייטרלי)', 'חיובי', 'נמוך יומי', 'גבוה יומי'],
                'המלצת מערכת': ['החזק', 'איסוף הדרגתי', 'נקודת כניסה', 'יעד חלקי']
            })
            st.dataframe(details_df, use_container_width=True)
        elif "2. ניתוח פונדמנטלי" in selected_method:
            details_df = pd.DataFrame({
                'פרמטר דוחות': ['הכנסות רבעוניות', 'רווח נקי', 'תשואת דיבידנד'],
                'נתון השוק': ['יציב', 'חיובי', '3.8% - 4.2%'],
                'הערכת שווי': ['תמחור הוגן', 'חזק', 'אטרקטיבי למשקיעים']
            })
            st.dataframe(details_df, use_container_width=True)
        else:
            details_df = pd.DataFrame({
                'מדד שוק': ['סיכון (Beta)', 'נזילות מסחר', 'סנטימנט כללי'],
                'נתון': ['1.05', 'גבוה מאוד', 'חיובי'],
                'סטטוס': ['תואם ענף', 'נזיל', 'תומך בעליות']
            })
            st.dataframe(details_df, use_container_width=True)

    else:
        st.error("אנא הזן שם מניה או סמל לפני לחיצה על כפתור הניתוח.")
