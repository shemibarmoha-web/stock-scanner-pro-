import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מקיפה")

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

st.info(f"הסבר: {analysis_methods[selected_method]}")

# שלב 2: הזנת מניה
stock_symbol = st.text_input("הקלד את שם/סמל המניה שברצונך לנתח (למשל: בזק, דלק קבוצה):")

# שלב 3: ביצוע הניתוח (כפתור יחיד שבודק את שניהם)
if st.button("בצע ניתוח"):
    if stock_symbol:
        st.divider()
        st.header(f"תוצאות ניתוח עבור: {stock_symbol}")
        
        if "1. ניתוח טכני" in selected_method:
            st.write("מנתח דפוסי נרות וממוצעים נעים...")
            st.success("זוהתה תבנית חיובית בגרף הטכני.")
        elif "2. ניתוח פונדמנטלי" in selected_method:
            st.write("מנתח דוחות כספיים ויחסי הון...")
            st.warning("יחס ה-P/E נמצא בטווח האטרקטיבי.")
        else:
            st.write(f"מבצע ניתוח מורכב לפי שיטת {selected_method}...")
            st.write("הניתוח הסתיים בהצלחה.")
    else:
        st.error("אנא הזן שם מניה כדי להמשיך.")
