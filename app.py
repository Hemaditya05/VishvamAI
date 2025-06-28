import os
import streamlit as st
import requests

# 1) UI boilerplate
st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️")
st.title("CyberSec Helper – HF Assistant Integration")

# 2) Show what secrets we actually have
st.write("🔑 st.secrets keys:", list(st.secrets.keys()))
st.write("🌐 ENV HUGGINGFACE_API_KEY:", os.getenv("HUGGINGFACE_API_KEY"))

# 3) Load API key safely
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("❌ Missing Hugging Face token. Add HUGGINGFACE_API_KEY in Streamlit Secrets or as an env var.")
    st.stop()

# 4) Your assistant ID from the “Direct URL”
ASSISTANT_ID = "685ee1a6eea0be4c99b8c12a"

# 5) Input box
question = st.text_area("Enter your cybersecurity question")
if not question:
    st.info("Type a question above")
elif st.button("Ask Assistant"):
    # 6) Send the request
    url = "https://api-inference.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"assistant_id": ASSISTANT_ID, "inputs": question}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
    except Exception as e:
        st.error(f"❌ Request error: {e}")
    else:
        st.write("📶 HTTP status:", resp.status_code)
        text = resp.text

        # 7) Parse JSON
        try:
            data = resp.json()
        except ValueError:
            st.error("❌ Invalid JSON response")
            st.write(text)
        else:
            # 8) If OK, extract content
            if resp.ok and "choices" in data:
                try:
                    answer = data["choices"][0]["message"]["content"]
                    st.success(answer)
                except Exception as e:
                    st.error(f"❌ Parse error: {e}")
                    st.write(data)
            else:
                st.error("❌ API returned an error")
                st.write(data)
