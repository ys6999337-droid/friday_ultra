import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="FRIDAY ULTRA", layout="centered")

st.title("🚀 FRIDAY ULTRA AI")
st.write("Live Crypto Signal Dashboard")

symbol = "BTC-USD"

@st.cache_data(ttl=300)
def get_data():
    df = yf.download(symbol, period="2d", interval="15m", progress=False)
    df = df.reset_index()
    return df

if st.button("Get Live Signal"):
    try:
        df = get_data()

        if df.empty:
            st.error("No Data Received")
        else:
            df["EMA9"] = df["Close"].ewm(span=9).mean()
            df["EMA21"] = df["Close"].ewm(span=21).mean()

            ema9 = df["EMA9"].iloc[-1]
            ema21 = df["EMA21"].iloc[-1]
            price = df["Close"].iloc[-1]

            if float(ema9) > float(ema21):
                st.success("BUY SIGNAL")
            else:
                st.error("SELL SIGNAL")

            st.write("Last Price:", round(float(price), 2))

    except Exception as e:
        st.error("Error: " + str(e))
