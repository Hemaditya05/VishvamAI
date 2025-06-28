import streamlit as st
import requests
import json

# Setup page
st.set_page_config(page_title="Cybersecurity Helper Bot", page_icon="🛡️")
st.title("🛡️ Cybersecurity Helper Bot")
st.markdown("Ask cybersecurity questions — powered by Hugging Face.")

# Load API key from Streamlit Secrets
API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
st.write("🔐 API Key loaded:", API_KEY is not None)

# Choose a model
MODEL_NAME = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# User input
user_input = st.text_area("💬 Enter your query here:")

if st.button("🚀 Get Response"):
    if not user_input.strip():
        st.warning("Please type a question.")
    else:
        with st.spinner("Getting response..."):
            try:
                payload = {
                    "inputs": user_input,
                    "options": {"wait_for_model": True}
                }
                response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
                result = response.json()

                # Check for output structure
                if isinstance(result, list) and "generated_text" in result[0]:
                    st.success(result[0]["generated_text"])
                elif "generated_text" in result:
                    st.success(result["generated_text"])
                elif "error" in result:
                    st.error(f"Hugging Face Error: {result['error']}")
                else:
                    st.warning("⚠️ Unexpected response format.")
            except Exception as e:
                st.error(f"API Request Failed: {str(e)}")

st.markdown("---")
st.caption("Built by Aditya | Streamlit + Hugging Face")
