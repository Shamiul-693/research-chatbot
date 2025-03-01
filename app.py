import streamlit as st
import google.generativeai as genai
import os
import docx  # For DOCX processing
import fitz  # PyMuPDF for PDF processing

# ✅ Securely load API key
api_key = os.getenv("AIzaSyCeFuy9rjWIlA3GqIJUBjLdqg2wa8BA7JM")  # Try environment variable first
if not api_key:
    try:
        api_key = st.secrets["gemini_api_key"]  # Try Streamlit Secrets
    except Exception:
        st.error("❌ Missing API Key! Set `GEMINI_API_KEY` as an environment variable or in Streamlit Secrets.")
        st.stop()

# ✅ Configure Google Gemini AI
genai.configure(api_key=api_key)

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = "\n".join([page.get_text("text") for page in doc])
            return text

        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text

        else:
            return "❌ Unsupported file format. Please upload a PDF or DOCX file."

# Streamlit UI
st.set_page_config(page_title="AI Research Chatbot", page_icon="🤖", layout="wide")

st.sidebar.title("🔍 Research Assistant Chatbot")
st.sidebar.write("💡Powered by Shamiul Islam [Facebook](https://www.facebook.com/samiulislam.693)")
st.sidebar.write("📄 Upload a research document and ask AI about it.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Messages
st.title("🚀 AI Research Assistant - SamBotChat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload your research paper (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
file_text = ""

if uploaded_file:
    file_text = extract_text_from_file(uploaded_file)
    if file_text:
        st.success("✅ File uploaded successfully!")
        st.text_area("Extracted Text (Preview):", file_text[:1000], height=150)

# User Input Section
user_input = st.chat_input("Type your question here...")
if user_input:
    full_prompt = f"Document Content:\n{file_text}\n\nUser Question:\n{user_input}" if file_text else user_input

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking... 🤖💭"):
        ai_response = chat_with_gemini(full_prompt)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    with st.chat_message("assistant"):
        st.markdown(ai_response)
