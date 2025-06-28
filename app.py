import os
import streamlit as st
from huggingface_hub import InferenceClient
from requests.exceptions import RequestException

# ─────────────────────────────────────────────────────────────
# 1) CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="CyberSec Helper", page_icon="🛡️", layout="wide")

# Custom CSS for a modern, professional look
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        color: #FFFFFF;
    }
    .stTextArea textarea {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #4CAF50;
        border-radius: 8px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        font-size: 18px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45A049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .response-box {
        background-color: #2A2A2A;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4CAF50;
        margin-top: 20px;
    }
    h1 {
        color: #4CAF50;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .sidebar .stButton>button {
        background-color: #2196F3;
        width: 100%;
        border-radius: 8px;
    }
    .sidebar .stButton>button:hover {
        background-color: #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

# 1a) Load your HF token from Streamlit secrets or env
HF_TOKEN = st.secrets.get("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_KEY")
if not HF_TOKEN:
    st.error("Missing HF token. Set HUGGINGFACE_API_KEY in Secrets or ENV.")
    st.stop()

# 1b) Instantiate a client
client = InferenceClient(api_key=HF_TOKEN)

# 1c) Your assistant’s model ID
MODEL_ID = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"

# ─────────────────────────────────────────────────────────────
# 2) UI
# ─────────────────────────────────────────────────────────────
st.title("🚀 CyberSec Helper")

# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    skill_level = st.selectbox("Your Skill Level", ["Beginner", "Intermediate", "Expert"])
    st.write("Adjust settings to tailor responses.")
    if st.button("Clear Input"):
        st.session_state.question = ""

# Main content
with st.container():
    st.markdown("### Ask Your Cybersecurity Question")
    question = st.text_area(
        "Enter your question here:",
        height=150,
        key="question",
        placeholder="e.g., How do I secure my web application from XSS attacks?"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Ask Bot", key="ask_button"):
            if question.strip():
                with st.spinner("Analyzing your question..."):
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
                        # Store response in session state
                        st.session_state.response = response.choices[0].message.content
                    except RequestException as e:
                        st.error(f"Network or auth error:\n{e}")
                    except Exception as e:
                        st.error(f"Unexpected error calling HF Inference API:\n{e}")
            else:
                st.warning("Please enter a question.")

    # Display response if available
    if "response" in st.session_state and st.session_state.response:
        st.markdown("<div class='response-box'>", unsafe_allow_html=True)
        st.markdown(f"**Assistant Response:** {st.session_state.response}")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #888;'> CyberSec Helper v1.0</p>",
    unsafe_allow_html=True
)
