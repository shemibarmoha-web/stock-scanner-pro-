import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")

# הזנת מניה
stock_symbol = st.text_input("הקלד את שם המניה:", value="דלק קבוצה")

# נתוני נרות יפניים לסימולציה
data = {
    'Date': ['2026-08-17', '2026-08-18', '2026-08-19', '2026-08-20', '2026-08-21'],
    'Open': [82.0, 83.5, 83.0, 84.2, 85.5],
    'High': [83.8, 84.5, 84.0, 86.2, 86.8],
    'Low': [81.5, 83.0, 82.5, 83.9, 85.1],
    'Close': [83.5, 83.0, 84.2, 86.15, 86.5]
}
df = pd.DataFrame(data)

st.header(f"🕯️ ניתוח טכני: {stock_symbol}")

# בניית הגרף היפני המקצועי
fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='Market Data'
)])

# הוספת תבנית "פטיש" (Hammer) כסימון על הגרף
fig.add_annotation(x='2026-08-19', y=82.5,
            text="Hammer 🔨",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=30)

fig.update_layout(
    title=f"גרף נרות יפניים - {stock_symbol}",
    yaxis_title="מחיר (₪)",
    xaxis_title="תאריך",
    template="plotly_dark",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)

# הסברים
st.success("""
### 💡 ניתוח תבניות נוכחי:
* **Hammer (פטיש):** זוהה בתאריך 19/08. זהו סימן היפוך שורי (Bullish) המעיד על כך שהמוכרים ניסו להוריד את המחיר, אך הקונים השתלטו וסגרו קרוב למחיר הפתיחה.
* **מגמה:** המניה נמצאת במומנטום חיובי עם נרות ירוקים רצופים (סגירה מעל הפתיחה).
* **סטטוס:** תמיכה חזקה באזור ה-82 ₪.
""")
