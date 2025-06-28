import streamlit as st
import requests

st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️")
st.title("CyberSec Helper")

API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
if not API_KEY:
    st.error("Missing API key")
    st.stop()

user_input = st.text_area("Enter your question")
if st.button("Get Response") and user_input:
    url = "https://api-inference.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "messages": [
            {"role": "system", "content": "You are an expert cybersecurity assistant."},
            {"role": "user",   "content": user_input}
        ]
    }

    resp = requests.post(url, headers=headers, json=payload)
    if not resp.ok:
        st.error(f"{resp.status_code}: {resp.text}")
    else:
        try:
            msg = resp.json()["choices"][0]["message"]["content"]
            st.success(msg)
        except Exception:
            st.error("Bad response format")
            st.write(resp.text)
