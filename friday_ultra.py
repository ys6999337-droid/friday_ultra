import streamlit as st
import requests

st.set_page_config(page_title="FRIDAY ULTRA", layout="centered")

st.title("🚀 FRIDAY ULTRA AI")
st.write("Live Crypto Signal Dashboard")

BASE_URL = "https://your-backend-url.onrender.com"

if st.button("Get Live Signal"):
    try:
        response = requests.get(f"{BASE_URL}/signal")
        data = response.json()

        st.subheader("Signal:")
        st.success(data["signal"])

        st.write("Confidence:", round(data["confidence"] * 100, 2), "%")
        st.write("RSI:", data["rsi"])

    except:
        st.error("Server not responding")

st.divider()

st.subheader("Multi Coin Scanner")

if st.button("Scan Market"):
    try:
        response = requests.get(f"{BASE_URL}/scan")
        coins = response.json()

        for coin in coins:
            st.write("---")
            st.write("Symbol:", coin["symbol"])
            st.write("Signal:", coin["signal"])
            st.write("Confidence:", round(coin["confidence"] * 100, 2), "%")
            st.write("Trend:", coin["trend"])
            st.write("Trade Allowed:", coin["allowed"])

    except:
        st.error("Scanner error")
