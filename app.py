import os, streamlit as st, requests

st.set_page_config("CyberSec Helper", "🛡️")
st.title("CyberSec Helper")

# use .get() instead of direct index
API_KEY = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not API_KEY:
    st.error("No API key found! Add HUGGINGFACE_API_KEY in your Secrets or env-var.")
    st.stop()

# input
q = st.text_area("Enter your question")
if st.button("Get Response") and q:
    r = requests.post(
        "https://api-inference.huggingface.co/v1/chat/completions",
        headers={"Authorization":f"Bearer {API_KEY}"},
        json={
            "model":"meta-llama/Llama-3.3-70B-Instruct",
            "messages":[
                {"role":"system","content":"You are an expert cybersecurity assistant."},
                {"role":"user","content":q}
            ]
        }
    )
    if r.status_code!=200:
        st.error(f"{r.status_code} {r.text}")
    else:
        try:
            answer = r.json()["choices"][0]["message"]["content"]
            st.success(answer)
        except:
            st.error("Bad response format")
            st.write(r.text)
