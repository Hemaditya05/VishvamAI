import os
import streamlit as st
import requests

st.set_page_config("CyberSec Helper", "🛡️")
st.title("CyberSec Helper – Debug")

# 1. Show secrets + env
st.write("🔑 st.secrets keys:", list(st.secrets.keys()))
st.write("🌐 ENV HUGGINGFACE_API_KEY:", os.getenv("HUGGINGFACE_API_KEY"))

# 2. Load key
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("❌ Missing API key")
    st.stop()

# 3. Ping your model
MODEL = "meta-llama/Llama-3.3-70B-Instruct"
ping_url = f"https://api-inference.huggingface.co/v1/models/{MODEL}"
ping = requests.get(ping_url, headers={"Authorization":f"Bearer {API_KEY}"})
st.write("🔍 Ping URL:", ping_url)
st.write("📶 Ping status:", ping.status_code)
st.write("🔄 Ping response:", ping.text)

# 4. Chat UI
q = st.text_area("Enter your question")
if st.button("Get Response") and q:
    post_url = "https://api-inference.huggingface.co/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a cybersecurity assistant."},
            {"role": "user",   "content": q}
        ]
    }
    r = requests.post(post_url, headers={"Authorization":f"Bearer {API_KEY}"}, json=payload)
    st.write("➡️ POST URL:", post_url)
    st.write("📶 POST status:", r.status_code)
    if not r.ok:
        st.error(r.text)
    else:
        try:
            data = r.json()
            answer = data["choices"][0]["message"]["content"]
            st.success(answer)
        except Exception:
            st.error("Bad response format")
            st.write(r.text)
