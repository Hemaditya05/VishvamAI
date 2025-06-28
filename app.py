import os, streamlit as st
import requests 
st.write("🔑 All secrets:", dict(st.secrets))  # see what keys Streamlit actually has

API_KEY = (
    st.secrets.get("HUGGINGFACE_API_KEY")
    or os.getenv("HUGGINGFACE_API_KEY")
)
st.write("✅ API key found:", bool(API_KEY))
if not API_KEY:
    st.error("No API key! → add HUGGINGFACE_API_KEY in **Manage app → Settings → Secrets** or set the env-var and redeploy.")
    st.stop()

# … rest of your code …


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
