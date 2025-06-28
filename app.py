import streamlit as st
import requests

API_KEY = st.secrets["HUGGINGFACE_API_KEY"]
st.write("API KEY Present:", API_KEY is not None)
MODEL_NAME = "tiiuae/falcon-7b-instruct"  # or your own model
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Cybersecurity Helper Bot", page_icon="🛡️")
st.title("🛡️ Cybersecurity Helper Bot")
st.markdown("Ask cybersecurity questions — powered by Hugging Face & Meta LLaMA.")

user_input = st.text_area("💬 Enter your query here:")

if st.button("🚀 Get Response"):
    if not user_input.strip():
        st.warning("Please type a question.")
    else:
        with st.spinner("Getting response..."):
            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={"inputs": user_input, "options": {"wait_for_model": True}}
                )
                result = response.json()
                if isinstance(result, list) and "generated_text" in result[0]:
                    st.success(result[0]["generated_text"])
                elif "generated_text" in result:
                    st.success(result["generated_text"])
                elif "error" in result:
                    st.error(f"Error from HF: {result['error']}")
                else:
                    st.warning("Unexpected response format.")
            except Exception as e:
                st.error(f"API Request Failed: {str(e)}")

st.markdown("---")
st.caption("Built by Aditya | Streamlit + Hugging Face")
