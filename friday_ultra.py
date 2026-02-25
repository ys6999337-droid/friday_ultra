import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="FRIDAY ULTRA", layout="centered")

st.title("🚀 FRIDAY ULTRA AI")
st.write("Live Crypto Signal Dashboard")

symbol = "BTC-USD"

@st.cache_data(ttl=300)
def get_data():
    data = yf.download(symbol, period="2d", interval="15m")
    return data

if st.button("Get Live Signal"):
    try:
        df = get_data()

        df["EMA9"] = df["Close"].ewm(span=9).mean()
        df["EMA21"] = df["Close"].ewm(span=21).mean()

        latest = df.iloc[-1]

        if latest["EMA9"] > latest["EMA21"]:
            st.success("BUY")
        else:
            st.error("SELL")

        st.write("Last Price:", round(latest["Close"],2))

    except Exception as e:
        st.error("Still Error: " + str(e))
