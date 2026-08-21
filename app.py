import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת")

# תפריט ניווט במסך הראשי (או בסרגל הצד)
analysis_page = st.radio(
    "בחר את מסך הניתוח הרצוי:",
    [
        "🕯️ 1. ניתוח נרות יפניים (Candlestick)",
        "📈 2. ניתוח טכני ומתנדים",
        "💰 3. ניתוח פונדמנטלי",
        "🔢 4. ניתוח כמותי",
        "📰 5. ניתוח סנטימנט שוק",
        "🌐 6. ניתוח Top-Down (מאקרו)"
    ]
)

st.divider()

# הזנת מניה משותפת לכל המסכים
stock_symbol = st.text_input("הקלד את שם/סמל המניה לניתוח (למשל: בזק, דלק קבוצה):", value="דלק קבוצה")

if stock_symbol:
    st.header(f"📊 מסך ניתוח: {stock_page_title(analysis_page)} עבור {stock_symbol}")
    
    # נתונים בסיסיים
    if "בזק" in stock_symbol:
        price, change, pe, mcap = "7.55 ₪", "-0.04%", "17.25", "20.8 מיליארד ₪"
    elif "דלק" in stock_symbol:
        price, change, pe, mcap = "86.15 ₪", "+5.58%", "11.2", "12.4 מיליארד ₪"
    else:
        price, change, pe, mcap = "120.50 ₪", "+1.20%", "14.5", "5.1 מיליארד ₪"

    col1, col2, col3 = st.columns(3)
    col1.metric("שער אחרון", price, change)
    col2.metric("מכפיל רווח (P/E)", pe)
    col3.metric("שווי שוק", mcap)

    st.divider()

    # הצגת תוכן בלעדי אך ורק למסך הנבחר
    if "נרות יפניים" in analysis_page:
        st.subheader("🕯️ ניתוח נרות יפניים והסבר מפורט")
        st.write("בגרף זה אנו מנתחים את התנהגות נרות המסחר היומיים כדי לזהות נקודות היפוך או המשכיות במגמה.")
        
        candles_df = pd.DataFrame({
            'תאריך': ['18/08', '19/08', '20/08'],
            'פתיחה': [445, 450, 452],
            'סגירה': [450, 452, 461],
            'תבנית שזוהתה': ['Hammer', 'Doji', 'Bullish Engulfing'],
            'פרשנות': ['התנגדות למוכרים', 'התלבטות בשוק', 'אות קנייה חזק (קונים השתלטו)']
        })
        st.dataframe(candles_df, use_container_width=True)
        st.success("💡 **הסבר מצב נוכחי:** נר הבליעה השורי (Bullish Engulfing) האחרון מראה שהקונים נכנסו בעוצמה ודחקו את המחיר מעלה מעל ממוצע הטווח הקצר.")

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 גרף מתנדים טכניים (RSI / MACD)")
        st.write("כאן מוצגים המדדים הטכניים הנגזרים מנפחי המסחר והמחירים ההיסטוריים.")
        
        chart_data = pd.DataFrame(np.random.randn(15, 2) * 3 + 100, columns=['מחיר מניה', 'ממוצע נע 50'])
        st.line_chart(chart_data)

        tech_df = pd.DataFrame({
            'מתנד': ['RSI (14)', 'MACD', 'תמיכה התנגדות'],
            'ערך': ['58.4 (נייטרלי-חיובי)', 'חיובי (+1.4)', 'תמיכה ב-82 ₪'],
            'פעולה נדרשת': ['החזק', 'איסוף', 'הגנת סטופ-לוס']
        })
        st.dataframe(tech_df, use_container_width=True)

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 ניתוח פונדמנטלי ודוחות כספיים")
        st.write("בדיקת הערך הכלכלי הפנימי של החברה בהתסמך על נתוני מאזן, רווח והפסד.")
        
        fund_df = pd.DataFrame({
            'מדד': ['P/E', 'תשואת דיבידנד', 'NAV (שווי נקי נכסי)', 'תזרים מזומנים'],
            'נתון': [pe, '4.2%', 'אטרקטיבי', 'חיובי ויציב'],
            'הערכה': ['מתמחר נכון', 'תשואה גבוהה', 'פוטנציאל אפסייד', 'יציבות פיננסית']
        })
        st.dataframe(fund_df, use_container_width=True)
        st.warning("💡 **הסבר פונדמנטלי:** החברה מציגה נתוני רווחיות יציבים התומכים בשער הנוכחי.")

    elif "כמותי" in analysis_page:
        st.subheader("🔢 ניתוח כמותי וסטטיסטיקות סיכון")
        st.write("מודלים מתמטיים להערכת תנודתיות, סטיית תקן וסיכון-סיכוי.")
        quant_df = pd.DataFrame({
            'מודל': ['סטיית תקן', 'Beta', 'VaR (סיכון יומי)'],
            'תוצאה': ['14.2% שנתי', '1.08', '-2.1%'],
            'משמעות': ['תנודתיות מתונה', 'נע בהתאם לשוק', 'רמת סיכון סבירה']
        })
        st.dataframe(quant_df, use_container_width=True)

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 סנטימנט משקיעים וניתוח חדשות")
        st.write("בחינת מצב הרוח הציבורי והתקשורתי כלפי המניה.")
        sent_df = pd.DataFrame({
            'מקור': ['חדשות כלכליות', 'רשתות חברתיות', 'מדד פחד/תאוות בצע'],
            'סנטימנט': ['חיובי מאוד', 'אופטימי', '62 (Greed)'],
            'השפעה': ['תמיכה בעליות', 'נפח מסחר ער', 'מומנטום חיובי']
        })
        st.dataframe(sent_df, use_container_width=True)

    else:
        st.subheader("🌐 ניתוח Top-Down (מאקרו וענפי)")
        st.write("ניתוח מלמעלה למטה: מסביבת המאקרו הכללית ועד למעמד החברה בענף.")
        top_down_df = pd.DataFrame({
            'שלב': ['מאקרו', 'ענף בבורסה', 'חברה מובילה'],
            'מצב': ['סביבת ריבית מתייצבת', 'צמיחה ענפית חיובית', 'נתח שוק מוביל'],
            'החלטה': ['השקעה מותרת', 'מומלץ להגדיל', 'מועדפת למעקב']
        })
        st.dataframe(top_down_df, use_container_width=True)

else:
    st.info("אנא הזן שם מניה כדי לצפות במסך הניתוח הנבחר.")

def stock_page_title(page_name):
    return page_name.split(". ")[1] if ". " in page_name else page_name
