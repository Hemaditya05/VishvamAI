import streamlit as st
import requests

st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️")
st.title("🛡️ CyberSec Helper")
st.markdown("Ask cybersecurity questions — powered by Hugging Face.")

API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct"
API_URL = "https://api-inference.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

user_input = st.text_area("💬 Enter your question:")

if st.button("🚀 Get Response"):
    if not user_input.strip():
        st.warning("Please type a question.")
    else:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are an expert cybersecurity assistant."},
                {"role": "user",   "content": user_input}
            ]
        }
        resp = requests.post(API_URL, headers=headers, json=payload)
        st.write("🔎 HTTP status:", resp.status_code)

        if resp.status_code != 200:
            st.error(f"{resp.status_code}: {resp.text}")
        else:
            try:
                data = resp.json()
            except ValueError:
                st.error("Invalid JSON response")
                st.write(resp.text)
            else:
                try:
                    reply = data["choices"][0]["message"]["content"]
                except Exception:
                    st.warning("Unexpected format:")
                    st.write(data)
                else:
                    st.success(reply)
