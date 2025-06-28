import streamlit as st
import requests

st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️")
st.title("🛡️ CyberSec Helper")
st.markdown("Ask cybersecurity questions — powered by Hugging Face.")

API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
st.write("🔐 API Key loaded:", API_KEY is not None)

# the model you chose
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct"

# 👇 the Chat Completions endpoint (note the /v1/ prefix)
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
        with st.spinner("Talking to the model…"):
            # build the OpenAI‐style messages payload
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "You are an expert cybersecurity assistant."},
                    {"role": "user",   "content": user_input}
                ]
            }

            resp = requests.post(API_URL, headers=headers, json=payload)
            st.write("🔎 HTTP status:", resp.status_code)
            data = resp.json()
            st.write("📦 raw result:", data)

            # parse out the assistant’s reply
            if resp.status_code == 200 and "choices" in data:
                reply = data["choices"][0]["message"]["content"]
                st.success(reply)
            elif resp.status_code == 401:
                st.error("❌ Unauthorized — check your token scopes.")
            elif resp.status_code == 404:
                st.error("❌ Model not found — make sure `MODEL_NAME` is exactly right and inference is enabled.")
            else:
                st.warning("⚠️ Unexpected response format; see the raw output above.")
