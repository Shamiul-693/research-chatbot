import streamlit as st
import google.generativeai as genai
import docx
import fitz  # PyMuPDF for PDF handling
import os

# Set up API key securely
genai.configure(api_key=st.secrets["AIzaSyCeFuy9rjWIlA3GqIJUBjLdqg2wa8BA7JM"])

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return "No file uploaded."

    file_type = uploaded_file.type

    if file_type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")  # Proper PDF handling
        text = "\n".join([page.get_text("text") for page in doc])
        return text if text.strip() else "⚠️ No readable text found in the PDF."

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else "⚠️ No readable text found in the DOCX."

    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    return "❌ Unsupported file format. Please upload a PDF, DOCX, or TXT file."

# Streamlit UI
st.set_page_config(page_title="AI Research Chatbot", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.title("🔍 Research Assistant Chatbot")
st.sidebar.write("💡 Powered by [Shamiul Islam](https://www.facebook.com/samiulislam.693)")
st.sidebar.write("📄 Upload a research document and ask AI about it.")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Messages
st.title("🚀 AI Research Assistant - SamBotChat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File Upload
uploaded_file = st.file_uploader("📂 Upload your research paper (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
file_text = extract_text_from_file(uploaded_file) if uploaded_file else ""

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    st.text_area("Extracted Text (Preview):", file_text[:1000], height=150)

# User Input Section
user_input = st.chat_input("Type your question here...")
if user_input:
    full_prompt = f"Document Content:\n{file_text}\n\nUser Question:\n{user_input}" if file_text else user_input

    # Append user message to session
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI Response
    with st.spinner("Thinking... 🤖💭"):
        ai_response = chat_with_gemini(full_prompt)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Option to Download Chat History
if st.sidebar.button("⬇️ Download Chat History"):
    chat_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    st.sidebar.download_button("Download Chat (.txt)", chat_history, "chat_history.txt")
