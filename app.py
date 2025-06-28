import os
import streamlit as st
import requests

st.set_page_config("CyberSec Helper", "🛡️")
st.title("🛡️ CyberSec Helper – Free Debug Version")

# 1) Show us what secrets/env we actually have
st.write("🔑 st.secrets keys:", list(st.secrets.keys()))
st.write("🌐 ENV HUGGINGFACE_API_KEY:", os.getenv("HUGGINGFACE_API_KEY"))

# 2) Load the key
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("❌ Missing API key. Set HUGGINGFACE_API_KEY in Streamlit Secrets or ENV.")
    st.stop()

# 3) Let me pick any model ID (default to gpt2 so we know it will work)
MODEL = st.text_input("Model ID", value="gpt2")

# 4) Prompt
prompt = st.text_area("Enter your question/prompt")
if not prompt:
    st.info("Type something above to generate.")
    
elif st.button("🚀 Generate"):
    # Decide which endpoint & payload
    if "chat" in MODEL.lower():
        url     = "https://api-inference.huggingface.co/chat/completions"
        payload = {"model": MODEL, "messages":[{"role":"user","content":prompt}]}
    else:
        url     = f"https://api-inference.huggingface.co/models/{MODEL}"
        payload = {"inputs": prompt}

    st.write("🔗 URL →", url)
    st.write("📦 Payload →", payload)

    # 5) Call
    r = requests.post(url, headers={"Authorization":f"Bearer {API_KEY}"}, json=payload)
    st.write("📶 Status →", r.status_code)

    if not r.ok:
        st.error("Error response:")
        st.write(r.text)
    else:
        # 6) Try to parse JSON
        try:
            out = r.json()
        except ValueError:
            st.error("Invalid JSON:")
            st.write(r.text)
            st.stop()

        st.write("📑 Raw output →", out)

        # 7) Display the text
        # chat style?
        if isinstance(out, dict) and "choices" in out:
            st.success(out["choices"][0]["message"]["content"])
        # text-gen style?
        elif isinstance(out, list) and "generated_text" in out[0]:
            st.success(out[0]["generated_text"])
        else:
            st.info("Unrecognized format, showing full JSON.")
            st.json(out)
