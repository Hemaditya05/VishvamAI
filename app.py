import os
import streamlit as st
import requests

st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️")
st.title("CyberSec Helper")

API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("Missing API key. Add HUGGINGFACE_API_KEY in Secrets or as an env-var.")
    st.stop()

MODEL = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
ENDPOINT = "https://api-inference.huggingface.co/v1/chat/completions"

q = st.text_area("Enter your question")
if st.button("Get Response") and q:
    resp = requests.post(
        ENDPOINT,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert cybersecurity assistant."},
                {"role": "user",   "content": q}
            ]
        }
    )
    if not resp.ok:
        st.error(f"{resp.status_code}: {resp.text}")
    else:
        data = resp.json()
        try:
            answer = data["choices"][0]["message"]["content"]
            st.success(answer)
        except Exception:
            st.error("Bad response format")
            st.write(data)
