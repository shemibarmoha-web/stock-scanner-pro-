import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת עם ויזואליזציה מלאה")

# תפריט בחירת מסך ניתוח
analysis_page = st.radio(
    "בחר את מסך הניתוח הרצוי:",
    [
        "🕯️ 1. ניתוח נרות יפניים",
        "📈 2. ניתוח טכני ומתנדים",
        "💰 3. ניתוח פונדמנטלי",
        "🔢 4. ניתוח כמותי",
        "📰 5. ניתוח סנטימנט שוק",
        "🌐 6. ניתוח Top-Down (מאקרו)"
    ]
)

st.divider()

# הזנת מניה
stock_symbol = st.text_input("הקלד את שם/סמל המניה לניתוח (למשל: בזק, דלק קבוצה):", value="דלק קבוצה")

if stock_symbol:
    st.header(f"📊 תוצאות עבור: {stock_symbol}")
    
    # נתונים בסיסיים
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

    # הצגת תוכן וגרפים ייעודיים בלבד לפי המסך הנבחר
    if "נרות יפניים" in analysis_page:
        st.subheader("🕯️ גרף ותבניות נרות יפניים")
        st.write("כאן מוצג ניתוח מחירי הפתיחה והסגירה היומיים לצורך זיהוי תבניות היפוך מומנטום.")
        
        # סימולציה ויזואלית של נרות (גרף עמודות מחירים)
        candles_chart_data = pd.DataFrame({
            'שער פתיחה': [445, 450, 452, 458],
            'שער סגירה': [450, 452, 461, 469]
        })
        st.bar_chart(candles_chart_data)
        
        st.markdown("""
        * **תבנית נוכחית:** Bullish Engulfing (בליעה שورية).
        * **הסבר מצב:** הנר הירוק האחרון בולע לחלוטין את הנר האדום שקדמו, מעיד על כוח קונים משמעותי ויציאה מאזור התנגדות.
        """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 גרף טכני וממוצעים נעים")
        st.write("מעקב אחר מגמות מחיר באמצעות אינדיקטורים טכניים ומתנדים.")
        
        tech_chart_data = pd.DataFrame(
            np.random.randn(20, 2) * 4 + 100,
            columns=['שער מניה', 'ממוצע נע 20']
        )
        st.line_chart(tech_chart_data)
        
        st.markdown("""
        * **RSI (14):** 58.4 (אזור נייטרלי הנוטה לעליות).
        * **MACD:** חיובי, תומך בהמשך מומנטום חיובי בטווח הקצר.
        """)

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 מודלים פונדמנטליים והערכת שווי")
        st.write("בדיקת שווי נקי נכסי (NAV), יחס P/E ותשואות דיבידנד.")
        
        fund_chart_data = pd.DataFrame({
            'ערך החברה': [100, 105, 112, 118]
        })
        st.area_chart(fund_chart_data)
        
        st.markdown(f"""
        * **יחס P/E נוכחי:** {pe} (מתמחר היטב את פוטנציאל הצמיחה).
        * **תשואת דיבידנד:** כ-4.2% לשנה, מתאים למשקיעי ערך.
        """)

    elif "כמותי" in analysis_page:
        st.subheader("🔢 מודלים כמותיים וסטטיסטיקה")
        st.write("ניתוח סטיית תקן, מדדי תנודתיות ומקדם סיכון Beta.")
        
        quant_chart_data = pd.DataFrame({
            'תנודתיות יומית': [1.2, 1.5, 0.9, 1.4, 1.1]
        })
        st.bar_chart(quant_chart_data)
        
        st.markdown("""
        * **Beta:** 1.08 (תנודתיות מתונה התואמת את ממוצע השוק).
        * **Value at Risk:** -2.1% במסגרת מרווח ביטחון של 95%.
        """)

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 מדדי סנטימנט וחדשות")
        st.write("סקירת הלך הרוח הציבורי והיקף השיח הכלכלי סביב המניה.")
        
        sent_chart_data = pd.DataFrame({
            'מדד אופטימיזציה': [50, 55, 62, 68]
        })
        st.line_chart(sent_chart_data)
        
        st.markdown("""
        * **מדד פחד ותאוות בצע:** 62 (Greed - אופטימיות זהירה).
        * **חדשות:** אזכורים חיוביים בדיווחים הכלכליים האחרונים.
        """)

    else:
        st.subheader("🌐 ניתוח Top-Down (מאקרו וענפי)")
        st.write("בחינת סביבת המאקרו והשפעתה על הענף והחברה הנבחרת.")
        
        macro_chart_data = pd.DataFrame({
            'מדד ענפי': [200, 205, 210, 218]
        })
        st.area_chart(macro_chart_data)
        
        st.markdown("""
        * **סביבת ריבית:** התייצבות התורמת להתרחבות פעילות עסקית.
        * **מעמד ענפי:** נתח שוק יציב ומוביל בתוך הסקטור.
        """)

else:
    st.info("אנא הזן שם מניה כדי לצפות במסך הניתוח.")
