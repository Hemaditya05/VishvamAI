import streamlit as st
import requests

st.set_page_config("CyberSec Helper", "🛡️")
st.title("🚀 CyberSec Helper")

# 1) Load your HF token
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("Missing HUGGINGFACE_API_KEY in Secrets")
    st.stop()

# 2) Your assistant’s ID from the Direct URL
ASSISTANT_ID = "685ee1a6eea0be4c99b8c12a"

# 3) UI
q = st.text_input("Ask your cybersecurity question:")
if st.button("Submit") and q:
    r = requests.post(
        "https://api-inference.huggingface.co/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"assistant_id": ASSISTANT_ID, "inputs": q}
    )
    if r.ok:
        reply = r.json()["choices"][0]["message"]["content"]
        st.markdown(f"**Bot:** {reply}")
    else:
        st.error(f"{r.status_code} {r.text}")
