import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro - מערכת ניתוח מתקדמת")
st.markdown("ברוכים הבאים למערכת הניתוח הטכני והפיננסי שלך.")

# --- סרגל צד או בחירה ראשית למשתמש ---
st.sidebar.header("⚙️ הגדרות ניתוח")

# בחירת מניה
stock_symbol = st.sidebar.text_input("הכנס סמל מניה (למשל: BEZQ.TA, DLEK.TA)", value="BEZQ.TA")

# בחירת שיטת ניתוח
analysis_method = st.sidebar.selectbox(
    "בחר שיטת ניתוח:",
    [
        "ניתוח נרות יפנים (Candlestick)",
        "ניתוח טכני ומתנדים (RSI / MACD)",
        "מודלים פיננסיים והערכת שווי (NAV / P/E)",
        "תבניות גרפיות (Chart Patterns)"
    ]
)

run_button = st.sidebar.button("הפעל ניתוח")

# --- אזור הצגת התוצאות ---
st.header(f"📊 תוצאות עבור: {stock_symbol.upper()}")

if run_button or stock_symbol:
    st.markdown(f"**שיטת הניתוח הנבחרת:** `{analysis_method}`")
    
    # סימולציית תוצאות בהתאם לבחירה
    if "נרות יפנים" in analysis_method:
        st.info("🕯️ **ניתוח נרות יפנים:** זוהתה תבנית היפוך (Bullish Engulfing). האות מצביע על אפשרות למומנטום חיובי בטווח הקצר.")
        # טבלת דמה לנרות
        candlestick_data = pd.DataFrame({
            'תאריך': ['2026-08-18', '2026-08-19', '2026-08-20'],
            'פתיחה': [510, 515, 512],
            'סגירה': [515, 512, 520],
            'מגמה': ['עולה', 'יורד', 'עולה חזק']
        })
        st.dataframe(candlestick_data, use_container_width=True)

    elif "טכני ומתנדים" in analysis_method:
        st.success("📈 **ניתוח טכני:** מדד ה-RSI עומד על 54.5 (אזור נייטרלי). ממוצע נע 50 חותך כלפי מעלה את ממוצע 200.")
        tech_df = pd.DataFrame({
            'אינדיקטור': ['RSI (14)', 'MACD', 'Support', 'Resistance'],
            'ערך': ['54.5 - נייטרלי', 'חיובי (+1.2)', '500 ₪', '540 ₪']
        })
        st.dataframe(tech_df, use_container_width=True)

    elif "מודלים פיננסיים" in analysis_method:
        st.warning("💰 **מודלים פיננסיים (NAV / P/E):** ניתוח שווי נקי נכסי ויחס מחיר לרווח.")
        valuation_df = pd.DataFrame({
            'מדד פיננסי': ['יחס P/E נוכחי', 'הערכת שווי NAV', 'תשואת דיבידנד'],
            'נתון': ['11.4', 'אטרקטיבי ביחס לשוק', '3.8%']
        })
        st.dataframe(valuation_df, use_container_width=True)

    else:
        st.info("📉 **תבניות גרפיות:** זוהתה תבנית תעלה עולה (Ascending Channel). רמת היציאה המומלצת מוגדרת בהתאם לסטופ-לוס אוותנטי.")
        patterns_df = pd.DataFrame({
            'תבנית': ['תעלה עולה', 'פריצת רמת התנגדות'],
            'סטטוס': ['פעילה', 'אושרה בהצלחה']
        })
        st.dataframe(patterns_df, use_container_width=True)

else:
    st.info("הכנס את פרטי המניה ובחר שיטת ניתוח בצד כדי להתחיל.")
