import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="FRIDAY ULTRA", layout="centered")

st.title("🚀 FRIDAY ULTRA AI")
st.write("Live Crypto Signal Dashboard")

symbol = "BTCUSDT"

@st.cache_data(ttl=300)
def get_data():
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])
    df["close"] = df["close"].astype(float)
    return df

if st.button("Get Live Signal"):
    try:
        df = get_data()

        df["ema9"] = df["close"].ewm(span=9).mean()
        df["ema21"] = df["close"].ewm(span=21).mean()

        latest = df.iloc[-1]

        if latest["ema9"] > latest["ema21"]:
            signal = "BUY"
            st.success("BUY")
        else:
            signal = "SELL"
            st.error("SELL")

        st.write("Last Price:", round(latest["close"],2))

    except:
        st.error("Data fetch error")
