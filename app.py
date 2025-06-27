import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Your Hugging Face model name or endpoint
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"  # Replace if using your own hosted model
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Streamlit UI setup
st.set_page_config(page_title="Cybersecurity Helper Bot", page_icon="🛡️")
st.title("🛡️ Cybersecurity Helper Bot")
st.markdown("Ask me anything about cybersecurity – tools, threats, practices, projects, etc.")

# Input box
user_input = st.text_area("💬 Enter your query here:", height=150)

# Button to send query
if st.button("🚀 Get Response"):
    if not user_input.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Thinking like a cybersecurity analyst..."):
            try:
                payload = {
                    "inputs": user_input,
                    "parameters": {
                        "max_new_tokens": 512,
                        "temperature": 0.7,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True
                    }
                }

                response = requests.post(API_URL, headers=headers, json=payload)
                result = response.json()

                # Process and display result
                if isinstance(result, list) and "generated_text" in result[0]:
                    st.success(result[0]["generated_text"])
                elif "generated_text" in result:
                    st.success(result["generated_text"])
                elif "error" in result:
                    st.error(f"⚠️ Hugging Face Error: {result['error']}")
                else:
                    st.error("⚠️ Unexpected response format.")
            except Exception as e:
                st.error(f"⚠️ API Request Failed: {str(e)}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Aditya | Meta LLaMA on Hugging Face + Streamlit UI")
