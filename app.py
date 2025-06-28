import os
import streamlit as st
import requests

# ─────────────────────────────────────────────────────────────
# 1) PAGE CONFIG & STYLING
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Cybersecurity Helper", layout="centered")

st.markdown("""
<style>
/* App background gradient */
.stApp {
  background: linear-gradient(135deg, #0f0f0f, #1f1f2f);
}

/* Title styling */
h1 {
  text-align: center;
  font-family: 'Helvetica Neue', sans-serif;
  color: #32CD32;
  margin-bottom: 1.5rem;
}

/* Button gradient */
.stButton>button {
  background: linear-gradient(90deg, #32CD32, #FF4500);
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  padding: 0.75em 1.5em;
  font-weight: 600;
  transition: background 0.3s ease;
}
.stButton>button:hover {
  background: linear-gradient(90deg, #FF4500, #32CD32);
}

/* Text area and input */
.stTextInput>div>div>input,
textarea {
  background-color: #2a2a3a;
  color: #e0e0e0;
  border: 1px solid #32CD32;
  border-radius: 0.25rem;
}

/* Success & error messages */
.stSuccess, .stError {
  border-radius: 0.25rem;
  padding: 0.75em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 2) HEADER
# ─────────────────────────────────────────────────────────────
st.title("Cybersecurity Helper")

# ─────────────────────────────────────────────────────────────
# 3) LOAD API KEY
# ─────────────────────────────────────────────────────────────
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("Missing Hugging Face API token. Please set HUGGINGFACE_API_KEY.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# 4) USER INPUT
# ─────────────────────────────────────────────────────────────
question = st.text_area("Enter your cybersecurity question:", height=150)
if st.button("Submit") and question.strip():
    # ─────────────────────────────────────────────────────────
    # 5) MAKE API CALL
    # ─────────────────────────────────────────────────────────
    url = "https://api-inference.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "mistralai/Mistral-Small-3.1-24B-Instruct-2503",
        "messages": [
            {"role": "system", "content": (
                "You are an expert cybersecurity architect, penetration tester, "
                "threat analyst, and project manager. Tailor your advice "
                "to my resources, skill level, time constraints, and goals."
            )},
            {"role": "user", "content": question}
        ]
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if not resp.ok:
        st.error(f"Error {resp.status_code}: {resp.text}")
    else:
        try:
            answer = resp.json()["choices"][0]["message"]["content"]
            st.success(answer)
        except Exception:
            st.error("Could not parse response.")
            st.write(resp.text)
