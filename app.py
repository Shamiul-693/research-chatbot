import streamlit as st
import google.generativeai as genai
import docx  # For DOCX processing
import fitz
# Set up API key (Replace with your actual API key)
genai.configure(api_key="AIzaSyCT-bvj0EJke7lBkGZRbeWF31v9XOSAHLg")

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.type

    # Extract text from PDF
    if file_type == "application/pdf":
        doc = PyMuPDF.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text

    # Extract text from DOCX
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    # Extract text from TXT
    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    else:
        return "⚠️ Unsupported file format. Please upload PDF, DOCX, or TXT."

# Streamlit UI with Chat History
st.set_page_config(page_title="AI Research Chatbot", page_icon="🤖", layout="wide")

# Sidebar
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

    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.spinner("Thinking... 🤖💭"):
        ai_response = chat_with_gemini(full_prompt)

    # Append AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
