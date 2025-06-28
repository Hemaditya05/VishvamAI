import os
import streamlit as st
import requests

st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️")
st.title("CyberSec Helper")

API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("Missing API key. Set HUGGINGFACE_API_KEY in Secrets or env.")
    st.stop()

model = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
endpoint = "https://api-inference.huggingface.co/v1/chat/completions"

q = st.text_area("Enter your question")
if st.button("Get Response") and q:
    r = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert cybersecurity assistant."},
                {"role": "user", "content": q}
            ]
        }
    )
    if not r.ok:
        st.error(f"{r.status_code}: {r.text}")
    else:
        try:
            answer = r.json()["choices"][0]["message"]["content"]
            st.success(answer)
        except:
            st.error("Bad response format")
            st.write(r.text)
