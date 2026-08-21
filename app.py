import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.markdown("ברוכים הבאים למערכת סריקת המניות והניתוח הטכני שלך.")

# נתוני דוגמה ראשוניים למערכת
data = {
    'מניה': ['דלק קבוצה', 'בזק', 'ליברה', 'דלק ייזום'],
    'מחיר (שקל)': [45000, 520, 630, 7100],
    'שינוי יומי (%)': [1.2, -0.5, 2.3, 0.8],
    'מגמה': ['עולה', 'יורד', 'עולה', 'עולה']
}

df = pd.DataFrame(data)

st.subheader("📊 סקירת מניות מובילות")
st.dataframe(df, use_container_width=True)

st.info("האפליקציה פועלת בהצלחה! כעת תוכל לחזור ל-Streamlit ולבצע Deploy מחדש.")
