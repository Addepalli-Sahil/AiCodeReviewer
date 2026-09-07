import streamlit as st
import requests
from pygments.lexers import guess_lexer, ClassNotFound
from io import BytesIO
import pdfkit
import markdown

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# --- Custom Style: Light Background Text Area ---
st.markdown(
    """
    <style>
    textarea, .stTextArea textarea {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Load API Key from Streamlit Secrets ---
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

# --- Model options ---
# --- Enhanced Model options ---
MODEL_OPTIONS = {
    # OpenAI Models
    "GPT-4o": "openai/gpt-4o",
    "GPT-4o Mini": "openai/gpt-4o-mini", 
    "GPT-4 Turbo": "openai/gpt-4-turbo",
    "GPT-4": "openai/gpt-4",
    
    # Anthropic Models (Excellent for code analysis)
    "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
    "Claude 3 Opus": "anthropic/claude-3-opus",
    "Claude 3 Haiku": "anthropic/claude-3-haiku",
    
    # Google Models
    "Gemini Pro 1.5": "google/gemini-pro-1.5",
    "Gemini Flash 1.5": "google/gemini-flash-1.5",
    
    # Meta Models (Cost-effective options)
    "Llama 3.1 70B": "meta-llama/llama-3.1-70b-instruct",
    "Llama 3.1 8B": "meta-llama/llama-3.1-8b-instruct",
    
    # Specialized Code Models
    "DeepSeek Coder V2": "deepseek/deepseek-coder",
    "Codestral": "mistralai/codestral-mamba"
}


# --- Helper Functions ---

def review_code_with_openrouter(code, model="gpt-4o-mini"):
    """
    Uses OpenRouter API to review the code and return suggestions.
    """
    prompt = f"Review this code and suggest improvements or errors:\n\n{code}"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert software engineer."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,  # Increase token limit for longer reviews
        "temperature": 0.2
    }

    try:
        response = requests.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error with OpenRouter API: {e}"

def detect_language(code):
    try:
        lexer = guess_lexer(code)
        return lexer.name.lower()
    except ClassNotFound:
        return None

def read_uploaded_file(uploaded_file) -> str:
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return None

def save_review_to_pdf(review_markdown: str) -> BytesIO:
    """
    Convert markdown review to styled HTML and render as PDF using pdfkit.
    """
    html_body = markdown.markdown(review_markdown, extensions=['fenced_code', 'codehilite'])

    full_html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            color: #000000;
            background-color: #ffffff;
            line-height: 1.6;
        }}
        h1 {{
            color: #2a7ae2;
            border-bottom: 3px solid #2a7ae2;
            padding-bottom: 10px;
        }}
        pre {{
            background: #f0f0f0;
            color: #000000;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.5;
            font-family: "Consolas", "Courier New", monospace;
        }}
        pre code {{
            color: inherit;
        }}
        code {{
            background: #f8f8f8;
            color: #000000;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: "Consolas", "Courier New", monospace;
        }}
        strong, b {{
            font-weight: bold;
        }}
        ul, ol {{
            margin-left: 20px;
        }}
        blockquote {{
            border-left: 4px solid #2a7ae2;
            margin: 10px 0;
            padding-left: 15px;
            color: #555555;
            font-style: italic;
        }}
        ::selection {{
            background: #2a7ae2;
            color: #ffffff;
        }}
        ::-moz-selection {{
            background: #2a7ae2;
            color: #ffffff;
        }}
    </style>
    </head>
    <body>
        <h1>AI Code Review Report</h1>
        {html_body}
    </body>
    </html>
    """

    options = {
        'page-size': 'A4',
        'dpi': 300,
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
        'quiet': ''
    }

    pdf_bytes = pdfkit.from_string(full_html, False, options=options)
    pdf_file = BytesIO(pdf_bytes)
    pdf_file.seek(0)
    return pdf_file

# --- App UI ---
st.title("🤖 AI Code Reviewer")

col1, col2 = st.columns([2, 3])

user_code = ""
file_content = ""

# --- Left Panel ---
with col1:
    st.header("Input Code")
    user_code = st.text_area("Paste your code here:", height=200)
    uploaded_file = st.file_uploader("Or upload a code file", type=["py", "js", "java", "cpp", "txt", "c", "html", "css"])

    if uploaded_file:
        file_content_read = read_uploaded_file(uploaded_file)
        if file_content_read is not None:
            file_content = file_content_read
            st.text_area("File content:", value=file_content, height=200)
        else:
            st.error("Could not read file. Please upload a text file.")

    selected_model_name = st.selectbox("Choose AI Model", options=list(MODEL_OPTIONS.keys()))
    selected_model = MODEL_OPTIONS[selected_model_name]

# --- Right Panel ---
with col2:
    st.header("Code Review")
    if st.button("Review Code"):
        code_to_review = user_code.strip() if user_code.strip() else file_content
        if code_to_review:
            with st.spinner("Analyzing your code... This may take a few seconds for larger inputs..."):
                review = review_code_with_openrouter(code_to_review, model=selected_model)
                lang = detect_language(code_to_review)

                if lang:
                    st.code(code_to_review, language=lang)
                else:
                    st.code(code_to_review)

                st.subheader("AI Review:")
                st.markdown(review)

                review_pdf = save_review_to_pdf(review)
                st.download_button(
                    label="📄 Download Review as PDF",
                    data=review_pdf,
                    file_name="code_review.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Please paste code or upload a file.")

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ by Sahil | Powered by OpenRouter & Streamlit")
