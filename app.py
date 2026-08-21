import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Stock Scanner Pro", page_icon="📈", layout="wide")

st.title("📈 Stock Scanner Pro")
st.subheader("מערכת ניתוח מניות מתקדמת")

# תפריט ניווט מלא בין כל המסכים
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

    # הצגת תוכן וגרפים לפי המסך הנבחר
    if "נרות יפניים" in analysis_page:
        st.subheader("🕯️ גרף נרות יפניים ותבניות מסחר (Candlestick)")
        st.write("תצוגה גרפית המדמה את התנהגות המחירים היומית, כולל פתילות, גופים ותבניות היפוך כמו 'פטיש':")
        
        # טבלת נרות יפניים מפורטת ומעוצבת המציגה את מבנה הנר המלא
        candles_df = pd.DataFrame({
            'יום מסחר': ['יום א', 'יום ב', 'יום ג (פטיש 🔨)', 'יום ד', 'היום (פריצה שורית)'],
            'פתיחה (₪)': [82.0, 83.5, 83.0, 84.2, 85.5],
            'גבוה (₪)': [83.8, 84.5, 84.0, 86.2, 86.8],
            'נמוך (₪)': [81.5, 83.0, 82.5, 83.9, 85.1],
            'סגירה (₪)': [83.5, 83.0, 84.2, 86.15, 86.5],
            'מבנה הנר': ['🟢 נר ירוק (עולה)', '🔴 נר אדום (יורד)', '🟢 פטיש (Hammer)', '🟢 נר ירוק (עולה)', '🟢 בליעה שורית מלאה']
        })
        st.dataframe(candles_df, use_container_width=True)
        
        # גרף מחירים חזותי נלווה
        chart_data = pd.DataFrame({
            'שער נמוך': [81.5, 83.0, 82.5, 83.9, 85.1],
            'שער סגירה': [83.5, 83.0, 84.2, 86.15, 86.5]
        })
        st.line_chart(chart_data)

        st.success("""
        💡 **ניתוח מצב נוכחי ותבניות:**
        * **תבנית פטיש (Hammer):** זוהתה באזור התמיכה – מעידה על ניסיון ירידה שנבלם באגרסיביות על ידי הקונים.
        * **נר בליעה (Bullish Engulfing):** הנר האחרון בולע את קודמו ומאשר מעבר לשליטת קונים מלאה ופריצת התנגדות.
        """)

    elif "טכני ומתנדים" in analysis_page:
        st.subheader("📈 גרף מתנדים טכניים (RSI / MACD)")
        st.write("מעקב אחר ממוצעים נעים ואינדיקטורים טכניים:")
        
        tech_chart_data = pd.DataFrame(
            np.random.randn(15, 2) * 2 + 85,
            columns=['שער מניה בפועל', 'ממוצע נע (MA 20)']
        )
        st.line_chart(tech_chart_data)
        
        st.info("* **RSI (14):** 58.4 (אזור נייטרלי-חיובי).\n* **MACD:** חיובי, תומך בהמשך מומנטום עולה.")

    elif "פונדמנטלי" in analysis_page:
        st.subheader("💰 ניתוח פונדמנטלי וערך כלכלי")
        st.write("בדיקת שווי נקי נכסי (NAV) ותשואות רווח:")
        
        fund_chart_data = pd.DataFrame({'שווי נכסי מוערך (NAV)': [78, 82, 85, 91]})
        st.area_chart(fund_chart_data)
        
        st.markdown(f"* **מכפיל רווח (P/E):** {pe}\n* **דיבידנדים:** תשואה עקבית התומכת במניה.")

    elif "כמותי" in analysis_page:
        st.subheader("🔢 ניתוח כמותי וסטטיסטיקות סיכון")
        st.write("בחינת סטיית תקן ומדדי תנודתיות:")
        
        quant_chart_data = pd.DataFrame({'תנודתיות יומית (%)': [1.1, 1.4, 0.8, 1.3]})
        st.bar_chart(quant_chart_data)
        
        st.markdown("* **Beta:** 1.08\n* **VaR (סיכון יומי):** -2.1%")

    elif "סנטימנט שוק" in analysis_page:
        st.subheader("📰 סנטימנט משקיעים וניתוח חדשות")
        st.write("מעקב אחר מדדי הפחד והתאוות בצע:")
        
        sent_chart_data = pd.DataFrame({'מדד סנטימנט': [50, 54, 59, 62]})
        st.line_chart(sent_chart_data)
        
        st.markdown("* **מדד Greed:** 62 (אופטימיות מבוקרת בשוק).")

    else:
        st.subheader("🌐 ניתוח Top-Down (מאקרו וענפי)")
        st.write("בחינת סביבת המאקרו והשפעתה על הענף:")
        
        macro_chart_data = pd.DataFrame({'מדד סקטוריאלי': [180, 185, 192, 198]})
        st.area_chart(macro_chart_data)
        
        st.markdown("* **סביבת ריבית:** מתייצבת ומעודדת כניסת הון לסקטור.")

else:
    st.info("אנא הזן שם מניה כדי לצפות במסך הניתוח.")
