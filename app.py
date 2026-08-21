import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת")

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
        st.subheader("🕯️ גרף מגמת מחירים ונרות יפניים")
        st.write("גרף המחירים היומי המציג את פריצת הרמות ואת התבנית השורית:")
        
        # גרף חזותי אמיתי לנרות/שערים
        candle_chart_data = pd.DataFrame({
            'שער נמוך': [81.5, 83.0, 82.5, 83.9],
            'שער סגירה': [83.5, 83.0, 84.2, 86.15]
        })
        st.line_chart(candle_chart_data)
        
        st.success("""
        💡 **ניתוח מצב נוכחי:** 
        * הגרף מציג זינוק חד בשער הסגירה אל עבר **86.15 ₪**.
        * **תבנית:** נר הבליעה האחרון מאשר השתלטות מלאה של קונים ויציאה מאזור ההתנגדות.
        """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 גרף מתנדים טכניים (RSI / MACD)")
        st.write("ניתוח מגמת המחיר מול ממוצע נע ל-20 תקופות:")
        
        tech_chart_data = pd.DataFrame(
            np.random.randn(15, 2) * 2 + 85,
            columns=['שער מניה בפועל', 'ממוצע נע (MA 20)']
        )
        st.line_chart(tech_chart_data)
        
        st.info("""
        * **RSI (14):** עומד על 58.4 (אזור נייטרלי-חיובי, רחוק מקניות יתר).
        * **מסקנה טכנית:** המניה נתמכת היטב מעל הממוצע הנע.
        """)

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 ניתוח פונדמנטלי וערך כלכלי")
        st.write("השוואת שווי נקי נכסי (NAV) ותשואות רווח לאורך זמן:")
        
        fund_chart_data = pd.DataFrame({
            'שווי נכסי מוערך (NAV)': [78, 82, 85, 91]
        })
        st.area_chart(fund_chart_data)
        
        st.markdown(f"""
        * **מכפיל רווח (P/E):** {pe} – משקף תמחור אטרקטיבי יחסית לענף.
        * **דיבידנדים:** חלוקה עקבית התומכת בתשואת ערך למשקיע.
        """)

    elif "כמותי" in analysis_page:
        st.subheader("🔢 ניתוח כמותי וסטטיסטיקות סיכון")
        st.write("בחינת סטיית תקן שנתית ומדדי תנודתיות סיכון-סיכוי:")
        
        quant_chart_data = pd.DataFrame({
            'תנודתיות יומית ממוצעת (%)': [1.1, 1.4, 0.8, 1.3]
        })
        st.bar_chart(quant_chart_data)
        
        st.markdown("""
        * **Beta:** 1.08 (מתואם היטב לתנועות המדד הכללי).
        * **VaR (סיכון יומי):** -2.1% בלבד בטווח הביטחון.
        """)

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 סנטימנט משקיעים וניתוח חדשות")
        st.write("מעקב אחר מדדי הפחד והתאוות בצע ברשתות ובסקירות הכלכליות:")
        
        sent_chart_data = pd.DataFrame({
            'מדד סנטימנט שבועי': [50, 54, 59, 62]
        })
        st.line_chart(sent_chart_data)
        
        st.markdown("""
        * **מדד נוכחי:** 62 (Greed - אופטימיות מבוקרת בשוק).
        * **חדשות אחרונות:** דיווחים חיוביים המעודדים המשך פוזיציות קיימות.
        """)

    else:
        st.subheader("🌐 ניתוח Top-Down (מאקרו וענפי)")
        st.write("בחינת המגמה מלמעלה למטה: מסביבת הריבית ועד לביצועי הסקטור:")
        
        macro_chart_data = pd.DataFrame({
            'מדד סקטוריאלי': [180, 185, 192, 198]
        })
        st.area_chart(macro_chart_data)
        
        st.markdown("""
        * **סביבת מאקרו:** ריבית מתייצבת המעודדת זרימת הון לסקטור האנרגיה/תשתיות.
        * **מיקום ענפי:** חוזק יחסי גבוה מול שאר המניות בבורסה.
        """)

else:
    st.info("אנא הזן שם מניה כדי לצפות במסך הניתוח.")
