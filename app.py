import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# =========================================================
# הגדרות עמוד
# =========================================================

st.set_page_config(
    page_title="מערכת ניתוח שוק ההון",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# יצירת נתוני שוק לדוגמה
# =========================================================

@st.cache_data
def generate_market_data(days=250):
    np.random.seed(42)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=days,
        freq="B"
    )

    returns = np.random.normal(0.0005, 0.018, days)

    close = 100 * np.exp(np.cumsum(returns))

    open_price = np.empty(days)
    open_price[0] = close[0] * np.random.uniform(0.99, 1.01)

    for i in range(1, days):
        open_price[i] = close[i - 1] * np.random.uniform(0.985, 1.015)

    high = np.maximum(open_price, close) * np.random.uniform(1.002, 1.03, days)
    low = np.minimum(open_price, close) * np.random.uniform(0.97, 0.998, days)

    volume = np.random.randint(500_000, 5_000_000, days)

    df = pd.DataFrame({
        "Date": dates,
        "Open": open_price,
        "High": high,
        "Low": low,
        "Close": close,
        "Volume": volume
    })

    return df


df = generate_market_data()


# =========================================================
# פונקציות לחישובים טכניים
# =========================================================

def calculate_rsi(series, period=14):
    delta = series.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()

    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line

    return macd, signal_line, histogram


def calculate_bollinger_bands(series, period=20, std_multiplier=2):
    sma = series.rolling(period).mean()
    std = series.rolling(period).std()

    upper = sma + std_multiplier * std
    lower = sma - std_multiplier * std

    return sma, upper, lower


# =========================================================
# זיהוי פטיש / פטיש הפוך
# =========================================================

def detect_candlestick_patterns(data):
    data = data.copy()

    body = abs(data["Close"] - data["Open"])
    candle_range = data["High"] - data["Low"]

    lower_shadow = np.minimum(data["Open"], data["Close"]) - data["Low"]
    upper_shadow = data["High"] - np.maximum(data["Open"], data["Close"])

    data["Hammer"] = (
        (lower_shadow >= body * 2) &
        (upper_shadow <= body * 0.8) &
        (candle_range > 0)
    )

    data["Inverted_Hammer"] = (
        (upper_shadow >= body * 2) &
        (lower_shadow <= body * 0.8) &
        (candle_range > 0)
    )

    return data


# =========================================================
# כותרת ראשית
# =========================================================

st.title("📊 מערכת מקצועית לניתוח מניות ושווקים")
st.markdown(
    "בחר שיטת ניתוח מהתפריט. כל שיטה נפתחת כדף עצמאי עם "
    "גרפים, נתונים, מדדים והסבר מקצועי."
)


# =========================================================
# תפריט ניווט
# =========================================================

with st.sidebar:
    st.header("🧭 ניווט")

    selected_page = st.radio(
        "בחר שיטת ניתוח:",
        [
            "🏠 דף ראשי",
            "1️⃣ גרף נרות יפניים ופטישים",
            "2️⃣ ניתוח טכני ומתנדים",
            "3️⃣ ניתוח פונדמנטלי / NAV",
            "4️⃣ ניתוח כמותי",
            "5️⃣ סנטימנט שוק"
        ]
    )

    st.divider()

    st.caption("מערכת הדגמה לניתוח נתוני שוק")


# =========================================================
# דף ראשי
# =========================================================

if selected_page == "🏠 דף ראשי":

    st.header("ברוכים הבאים למערכת")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "מחיר אחרון",
        f"{df['Close'].iloc[-1]:.2f}"
    )

    daily_change = (
        (df["Close"].iloc[-1] / df["Close"].iloc[-2]) - 1
    ) * 100

    col2.metric(
        "שינוי יומי",
        f"{daily_change:.2f}%"
    )

    total_change = (
        (df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1
    ) * 100

    col3.metric(
        "שינוי בתקופה",
        f"{total_change:.2f}%"
    )

    st.divider()

    st.subheader("מה כוללת המערכת?")

    st.markdown("""
    ### 🕯️ נרות יפניים
    זיהוי תבניות נרות, פטישים, פטישים הפוכים ונקודות היפוך אפשריות.

    ### 📉 ניתוח טכני
    RSI, MACD, ממוצעים נעים ורצועות בולינגר.

    ### 💰 ניתוח פונדמנטלי
    NAV, שווי נכסים, חוב, מזומן ויחסי תמחור.

    ### 📐 ניתוח כמותי
    תשואות, תנודתיות, מומנטום, ממוצעים סטטיסטיים ומדדי סיכון.

    ### 🧠 סנטימנט שוק
    מדד סנטימנט משוקלל המדמה מצב של פחד, ניטרליות או חמדנות.
    """)


# =========================================================
# 1. נרות יפניים ופטישים
# =========================================================

elif selected_page == "1️⃣ גרף נרות יפניים ופטישים":

    st.header("🕯️ ניתוח נרות יפניים וזיהוי פטישים")

    data = detect_candlestick_patterns(df)

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=data["Date"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="מחיר"
        )
    )

    hammer_data = data[data["Hammer"]]

    fig.add_trace(
        go.Scatter(
            x=hammer_data["Date"],
            y=hammer_data["Low"] * 0.985,
            mode="markers",
            name="Hammer",
            marker=dict(
                size=12,
                symbol="triangle-up"
            )
        )
    )

    inverted_data = data[data["Inverted_Hammer"]]

    fig.add_trace(
        go.Scatter(
            x=inverted_data["Date"],
            y=inverted_data["High"] * 1.015,
            mode="markers",
            name="Inverted Hammer",
            marker=dict(
                size=12,
                symbol="triangle-down"
            )
        )
    )

    fig.update_layout(
        title="גרף נרות יפניים עם זיהוי תבניות",
        xaxis_title="תאריך",
        yaxis_title="מחיר",
        height=700,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📖 הסבר מקצועי על התוצאה")

    latest_hammer = data[data["Hammer"]].tail(1)
    latest_inverted = data[data["Inverted_Hammer"]].tail(1)

    if not latest_hammer.empty:
        date = latest_hammer["Date"].iloc[0].strftime("%d/%m/%Y")
        st.success(
            f"🔨 זוהתה תבנית פטיש. הזיהוי האחרון היה בתאריך {date}."
        )

        st.markdown("""
        **פירוש מקצועי:** פטיש עשוי להצביע על כך שהמחיר ירד במהלך
        המסחר, אך קונים נכנסו והחזירו את המחיר כלפי מעלה. כאשר התבנית
        מופיעה לאחר ירידה ובאישור של נר עולה נוסף, היא יכולה להעיד על
        אפשרות להיפוך מגמה.
        """)

    if not latest_inverted.empty:
        date = latest_inverted["Date"].iloc[0].strftime("%d/%m/%Y")
        st.info(
            f"🔨 זוהתה גם תבנית פטיש הפוך. הזיהוי האחרון היה בתאריך {date}."
        )

    if latest_hammer.empty and latest_inverted.empty:
        st.warning(
            "לא זוהתה לאחרונה תבנית פטיש מובהקת לפי תנאי הזיהוי שהוגדרו."
        )

    st.subheader("📋 נתוני הנרות האחרונים")

    st.dataframe(
        data[
            [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Hammer",
                "Inverted_Hammer"
            ]
        ].tail(20),
        use_container_width=True
    )


# =========================================================
# 2. ניתוח טכני ומתנדים
# =========================================================

elif selected_page == "2️⃣ ניתוח טכני ומתנדים":

    st.header("📉 ניתוח טכני ומתנדים")

    data = df.copy()

    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()

    data["RSI"] = calculate_rsi(data["Close"])

    macd, signal_line, histogram = calculate_macd(data["Close"])

    data["MACD"] = macd
    data["Signal"] = signal_line
    data["Histogram"] = histogram

    middle, upper, lower = calculate_bollinger_bands(data["Close"])

    data["BB_Middle"] = middle
    data["BB_Upper"] = upper
    data["BB_Lower"] = lower

    # -------------------------------
    # גרף מחיר וממוצעים
    # -------------------------------

    fig_price = go.Figure()

    fig_price.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Close"],
            name="מחיר סגירה"
        )
    )

    fig_price.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["MA20"],
            name="MA20"
        )
    )

    fig_price.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["MA50"],
            name="MA50"
        )
    )

    fig_price.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["BB_Upper"],
            name="Bollinger Upper"
        )
    )

    fig_price.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["BB_Lower"],
            name="Bollinger Lower"
        )
    )

    fig_price.update_layout(
        title="מחיר, ממוצעים נעים ורצועות בולינגר",
        height=550
    )

    st.plotly_chart(fig_price, use_container_width=True)

    # -------------------------------
    # RSI
    # -------------------------------

    fig_rsi = go.Figure()

    fig_rsi.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["RSI"],
            name="RSI"
        )
    )

    fig_rsi.add_hline(y=70, line_dash="dash")
    fig_rsi.add_hline(y=30, line_dash="dash")
    fig_rsi.add_hline(y=50, line_dash="dot")

    fig_rsi.update_layout(
        title="RSI - מדד עוצמה יחסית",
        yaxis_range=[0, 100],
        height=350
    )

    st.plotly_chart(fig_rsi, use_container_width=True)

    # -------------------------------
    # MACD
    # -------------------------------

    fig_macd = go.Figure()

    fig_macd.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["Histogram"],
            name="Histogram"
        )
    )

    fig_macd.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["MACD"],
            name="MACD"
        )
    )

    fig_macd.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Signal"],
            name="Signal"
        )
    )

    fig_macd.update_layout(
        title="MACD",
        height=400
    )

    st.plotly_chart(fig_macd, use_container_width=True)

    # -------------------------------
    # ניתוח מקצועי
    # -------------------------------

    st.subheader("📖 הסבר מקצועי על התוצאות")

    latest = data.iloc[-1]

    rsi_value = latest["RSI"]

    if rsi_value > 70:
        rsi_text = (
            f"RSI עומד על {rsi_value:.2f}, רמה גבוהה מ-70. "
            "הנכס נמצא באזור קניית יתר, ולכן קיימת אפשרות להתקררות או תיקון."
        )

    elif rsi_value < 30:
        rsi_text = (
            f"RSI עומד על {rsi_value:.2f}, רמה נמוכה מ-30. "
            "הנכס נמצא באזור מכירת יתר, מה שעשוי להצביע על אפשרות לריבאונד."
        )

    else:
        rsi_text = (
            f"RSI עומד על {rsi_value:.2f}, כלומר השוק נמצא כרגע "
            "באזור ניטרלי ללא מצב קיצון ברור."
        )

    st.markdown(f"**RSI:** {rsi_text}")

    if latest["MA20"] > latest["MA50"]:
        trend_text = (
            "הממוצע הנע הקצר MA20 נמצא מעל MA50, "
            "וזה מצביע על מומנטום חיובי בטווח הקצר."
        )
    else:
        trend_text = (
            "הממוצע הנע הקצר MA20 נמצא מתחת ל-MA50, "
            "מה שמצביע על חולשה יחסית בטווח הקצר."
        )

    st.markdown(f"**מגמה:** {trend_text}")

    if latest["MACD"] > latest["Signal"]:
        macd_text = (
            "קו ה-MACD נמצא מעל קו האיתות, דבר התומך במומנטום חיובי."
        )
    else:
        macd_text = (
            "קו ה-MACD נמצא מתחת לקו האיתות, דבר המעיד על מומנטום חלש יותר."
        )

    st.markdown(f"**MACD:** {macd_text}")

    st.subheader("📋 טבלת המדדים")

    indicators_table = pd.DataFrame({
        "מדד": ["מחיר אחרון", "MA20", "MA50", "RSI", "MACD", "Signal"],
        "ערך": [
            latest["Close"],
            latest["MA20"],
            latest["MA50"],
            latest["RSI"],
            latest["MACD"],
            latest["Signal"]
        ]
    })

    st.dataframe(indicators_table, use_container_width=True)


# =========================================================
# 3. ניתוח פונדמנטלי / NAV
# =========================================================

elif selected_page == "3️⃣ ניתוח פונדמנטלי / NAV":

    st.header("💰 ניתוח פונדמנטלי ו-NAV")

    st.info(
        "המספרים בדוגמה זו הם נתונים מדומים. "
        "במערכת אמיתית יש לחבר API או קובץ נתונים פיננסי."
    )

    total_assets = 5_200_000_000
    cash = 850_000_000
    investments = 3_100_000_000
    debt = 1_400_000_000
    other_liabilities = 350_000_000
    shares_outstanding = 500_000_000
    market_cap = 4_300_000_000

    total_liabilities = debt + other_liabilities

    nav = total_assets - total_liabilities
    nav_per_share = nav / shares_outstanding

    market_price_per_share = market_cap / shares_outstanding

    premium_discount = (
        (market_price_per_share / nav_per_share) - 1
    ) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "NAV כולל",
        f"{nav / 1_000_000_000:.2f} מיליארד"
    )

    col2.metric(
        "NAV למניה",
        f"{nav_per_share:.2f}"
    )

    col3.metric(
        "מחיר שוק למניה",
        f"{market_price_per_share:.2f}"
    )

    col4.metric(
        "פרמיה / דיסקאונט ל-NAV",
        f"{premium_discount:.2f}%"
    )

    # -------------------------------
    # גרף נכסים מול התחייבויות
    # -------------------------------

    categories = [
        "נכסים",
        "מזומן",
        "השקעות",
        "חוב",
        "התחייבויות אחרות"
    ]

    values = [
        total_assets,
        cash,
        investments,
        debt,
        other_liabilities
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values
            )
        ]
    )

    fig.update_layout(
        title="מבנה פיננסי של החברה",
        yaxis_title="שווי כספי",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📖 הסבר מקצועי")

    if premium_discount < 0:
        explanation = (
            f"המניה נסחרת בדיסקאונט של {abs(premium_discount):.2f}% "
            "לעומת ה-NAV המחושב. תיאורטית, זה עשוי להצביע על תמחור חסר, "
            "אך חשוב לבדוק את איכות הנכסים, רמת הנזילות, החוב והסיכונים."
        )
    else:
        explanation = (
            f"המניה נסחרת בפרמיה של {premium_discount:.2f}% "
            "לעומת ה-NAV. המשקיעים מתמחרים את החברה מעל השווי הנכסי הנקי."
        )

    st.markdown(explanation)

    debt_to_assets = debt / total_assets * 100

    st.markdown(
        f"**יחס חוב לנכסים:** {debt_to_assets:.2f}%"
    )

    if debt_to_assets > 50:
        st.warning(
            "רמת המינוף גבוהה יחסית. יש לבדוק את יכולת החברה לשרת את החוב."
        )
    else:
        st.success(
            "רמת המינוף נמצאת ברמה סבירה ביחס למבנה הנכסים בדוגמה."
        )

    st.subheader("📋 טבלת נתונים פונדמנטליים")

    fundamental_table = pd.DataFrame({
        "פרמטר": [
            "סך נכסים",
            "מזומן",
            "השקעות",
            "חוב",
            "התחייבויות אחרות",
            "NAV",
            "מספר מניות",
            "NAV למניה"
        ],
        "ערך": [
            total_assets,
            cash,
            investments,
            debt,
            other_liabilities,
            nav,
            shares_outstanding,
            nav_per_share
        ]
    })

    st.dataframe(fundamental_table, use_container_width=True)


# =========================================================
# 4. ניתוח כמותי
# =========================================================

elif selected_page == "4️⃣ ניתוח כמותי":

    st.header("📐 ניתוח כמותי וסטטיסטי")

    data = df.copy()

    data["Daily_Return"] = data["Close"].pct_change()
    data["Log_Return"] = np.log(
        data["Close"] / data["Close"].shift(1)
    )

    data["Rolling_Volatility"] = (
        data["Daily_Return"]
        .rolling(20)
        .std()
        * np.sqrt(252)
    )

    data["Momentum_20"] = (
        data["Close"] / data["Close"].shift(20) - 1
    ) * 100

    annual_return = (
        (data["Close"].iloc[-1] / data["Close"].iloc[0])
        ** (252 / len(data))
        - 1
    )

    annual_volatility = (
        data["Daily_Return"].std() * np.sqrt(252)
    )

    sharpe_ratio = (
        annual_return / annual_volatility
        if annual_volatility != 0
        else 0
    )

    max_drawdown_series = (
        data["Close"] / data["Close"].cummax() - 1
    )

    max_drawdown = max_drawdown_series.min()

    # -------------------------------
    # גרף תשואה מצטברת
    # -------------------------------

    data["Cumulative_Return"] = (
        (1 + data["Daily_Return"]).cumprod() - 1
    ) * 100

    fig_return = go.Figure()

    fig_return.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Cumulative_Return"],
            name="תשואה מצטברת"
        )
    )

    fig_return.update_layout(
        title="תשואה מצטברת",
        yaxis_title="תשואה %",
        height=450
    )

    st.plotly_chart(fig_return, use_container_width=True)

    # -------------------------------
    # גרף תנודתיות
    # -------------------------------

    fig_volatility = go.Figure()

    fig_volatility.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Rolling_Volatility"] * 100,
            name="תנודתיות שנתית"
        )
    )

    fig_volatility.update_layout(
        title="תנודתיות מתגלגלת ל-20 ימים",
        yaxis_title="תנודתיות %",
        height=400
    )
