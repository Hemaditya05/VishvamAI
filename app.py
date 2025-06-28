import os
import streamlit as st
from huggingface_hub import InferenceClient
from requests.exceptions import RequestException

# ─────────────────────────────────────────────────────────────
# 1) CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config("CyberSec Helper", "🛡️")
st.title("🚀 CyberSec Helper (InferenceClient)")

# 1a) Load your HF token from Streamlit secrets or env
HF_TOKEN = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not HF_TOKEN:
    st.error("Missing HF token. Set HUGGINGFACE_API_KEY in Secrets or ENV.")
    st.stop()

# 1b) Instantiate a client (it will pick Fireworks, Novita, or fallback)
client = InferenceClient(api_key=HF_TOKEN)

# 1c) Your assistant’s model (or base model) ID
MODEL_ID = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"

# ─────────────────────────────────────────────────────────────
# 2) UI
# ─────────────────────────────────────────────────────────────
question = st.text_area("Enter your cybersecurity question:")
if st.button("Ask Bot") and question.strip():
    with st.spinner("Thinking…"):
        try:
            # ─────────────────────────────────────────────────────
            # 3) Call the chat endpoint
            # ─────────────────────────────────────────────────────
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert cybersecurity architect, penetration tester, "
                            "threat analyst, and project manager. Tailor your advice to my "
                            "resources, skill level, time constraints, and research goals."
                        )
                    },
                    {"role": "user", "content": question}
                ]
            )
        except RequestException as e:
            st.error(f"Network or auth error:\n{e}")
        except Exception as e:
            st.error(f"Unexpected error calling HF Inference API:\n{e}")
        else:
            # ─────────────────────────────────────────────────────
            # 4) Extract and show the assistant’s reply
            # ─────────────────────────────────────────────────────
            try:
                reply = response.choices[0].message.content
                st.markdown(f"**Assistant:**  {reply}")
            except Exception:
                st.error("Failed to parse response:")
                st.json(response)
