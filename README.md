

# 🛡️ CyberSec Helper  

An AI-powered **cybersecurity assistant** built with **Streamlit** and **Hugging Face Inference API**.  
It helps users — from **beginners to experts** — ask cybersecurity-related questions and receive tailored guidance on topics like **web security, ethical hacking, threat analysis, penetration testing, and secure architecture design**.  

---

## 🚀 Features  

- **Interactive Web UI**: Built using [Streamlit](https://streamlit.io) with a **dark modern theme**.  
- **Skill-Level Personalization**: Beginner, Intermediate, and Expert modes to adjust response depth.  
- **Hugging Face Integration**: Powered by `mistralai/Mistral-Small-3.1-24B-Instruct-2503`.  
- **Responsive Design**: Sidebar for settings, styled text areas, and clean response boxes.  
- **Error Handling**: Friendly messages for missing tokens, auth issues, and network errors.  
- **Secure API Key Management**: Supports both **Streamlit secrets** and environment variables.  

---

## 📂 Project Structure  

```

CyberSec-Helper/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

````

---

## ⚙️ Installation & Setup  

### 1. Clone Repository  
```bash
git clone https://github.com/yourusername/cybersec-helper.git
cd cybersec-helper
````

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Authentication Setup

This app requires a Hugging Face **API Key**.

1. Get your key from [Hugging Face Settings → Access Tokens](https://huggingface.co/settings/tokens).
2. Set it up in one of the following ways:

* **Option A: Streamlit Secrets (Preferred)**
  Create a `.streamlit/secrets.toml` file:

  ```toml
  HUGGINGFACE_API_KEY = "your_hf_api_key_here"
  ```

* **Option B: Environment Variable**

  ```bash
  export HUGGINGFACE_API_KEY="your_hf_api_key_here"   # Linux / Mac
  setx HUGGINGFACE_API_KEY "your_hf_api_key_here"    # Windows
  ```

---

## ▶️ Running the App

Run locally:

```bash
streamlit run app.py
```

The app will start at **[http://localhost:8501](http://localhost:8501)**

---

## 🎨 UI Showcase

### Main Page

* Title: **CyberSec Helper**
* Input Box: Type your cybersecurity question
* Button: *Ask Bot*
* Response Box: Displays AI-generated answer

### Sidebar

* Skill level selector (**Beginner / Intermediate / Expert**)
* Button to clear input

---

## 📘 Example Usage

**User Input:**

> How do I secure my web application from SQL injection?

**CyberSec Helper Response (Beginner Mode):**

* Use **parameterized queries** instead of string concatenation.
* Avoid dynamic SQL queries.
* Implement **input validation and sanitization**.
* Deploy a **Web Application Firewall (WAF)**.

---

## 🛠️ Technologies Used

* [Streamlit](https://streamlit.io/) – for interactive UI
* [Hugging Face Inference API](https://huggingface.co/) – for AI responses
* [Mistral Small 3.1 24B Instruct](https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503) – underlying LLM
* [Python](https://www.python.org/) – core programming language

---

## 🧑‍💻 Roadmap

* [ ] Add **context-aware memory** (remember past questions per session)
* [ ] Implement **download/export response as PDF**
* [ ] Add **voice input/output** for accessibility
* [ ] Integrate **OWASP Top 10 quick tips mode**
* [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
 

## 💡 Acknowledgments

* Hugging Face for hosting cutting-edge AI models.
* MistralAI team for building **Mistral-Small-3.1-24B**.
* Streamlit community for awesome UI support
