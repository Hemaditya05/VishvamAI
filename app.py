import os
import streamlit as st
import requests

st.set_page_config("CyberSec Helper", "🛡️")
st.title("CyberSec Helper – Debug Mode")

# 1. Show loaded secrets and environment
st.write("🔑 st.secrets:", dict(st.secrets))
st.write("🌐 ENV HUGGINGFACE_API_KEY:", os.getenv("HUGGINGFACE_API_KEY"))

# 2. Load API key
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("Missing API key")
    st.stop()

# 3. Ping a known public model to verify auth & endpoint
ping = requests.get(
    "https://api-inference.huggingface.co/models/gpt2",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
try:
    st.write("Ping gpt2:", ping.status_code, ping.json())
except:
    st.write("Ping gpt2 invalid JSON:", ping.status_code, ping.text)

# 4. User input
q = st.text_area("Enter your question")
if not q:
    st.info("Type something above")
elif st.button("Debug & Get Response"):
    url = "https://api-inference.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "messages": [
            {"role": "system", "content": "You are an expert cybersecurity assistant."},
            {"role": "user",   "content": q}
        ]
    }

    resp = requests.post(url, headers=headers, json=payload)
    st.write("POST status:", resp.status_code)
    try:
        data = resp.json()
        st.json(data)
    except:
        st.write("Invalid JSON response:", resp.text)
        st.stop()

    # parse
    try:
        answer = data["choices"][0]["message"]["content"]
        st.success(answer)
    except Exception as e:
        st.error(f"Parse error: {e}")
        st.write(data)
