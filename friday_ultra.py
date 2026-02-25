import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="FRIDAY ULTRA PRO", layout="centered")

st.title("🚀 FRIDAY ULTRA AI PRO")
st.write("Advanced Live Crypto Signal Dashboard")

# ---- Coin Selection ----
coin = st.selectbox("Select Coin", ["BTC-USD", "ETH-USD", "SOL-USD"])

@st.cache_data(ttl=120)
def get_data(symbol):
    df = yf.download(symbol, period="3d", interval="15m", progress=False)
    df = df.reset_index()
    return df

# ---- RSI Function ----
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

if st.button("Generate Signal"):
    df = get_data(coin)

    if df.empty:
        st.error("No data received")
    else:
        df["EMA9"] = df["Close"].ewm(span=9).mean()
        df["EMA21"] = df["Close"].ewm(span=21).mean()
        df["RSI"] = calculate_rsi(df["Close"])

        ema9 = df["EMA9"].iloc[-1]
        ema21 = df["EMA21"].iloc[-1]
        rsi = df["RSI"].iloc[-1]
        price = df["Close"].iloc[-1]

        # ---- Smart Logic ----
        if ema9 > ema21 and rsi > 55:
            signal = "🔥 STRONG BUY"
            confidence = 85
            st.success(signal)
        elif ema9 > ema21:
            signal = "BUY"
            confidence = 65
            st.success(signal)
        elif ema9 < ema21 and rsi < 45:
            signal = "🚨 STRONG SELL"
            confidence = 85
            st.error(signal)
        else:
            signal = "SELL"
            confidence = 60
            st.error(signal)

        st.write("### 💰 Last Price:", round(price,2))
        st.write("### 📊 RSI:", round(rsi,2))
        st.write("### 🎯 Confidence:", f"{confidence}%")

        # ---- Chart Safe Version ----
try:
    if "Datetime" in df.columns:
        df_chart = df.set_index("Datetime")
    elif "Date" in df.columns:
        df_chart = df.set_index("Date")
    else:
        df_chart = df

    st.line_chart(df_chart[["Close","EMA9","EMA21"]])
except:
    st.warning("Chart not available")
