import streamlit as st
import google.generativeai as genai
import docx
import fitz

# Configure API key from Streamlit secrets
genai.configure(api_key=st.secrets["AIzaSyCeFuy9rjWIlA3GqIJUBjLdqg2wa8BA7JM"])

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text("text")
                return text
            except Exception as e:
                return f"Error processing PDF: {e}"

        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            try:
                doc = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            except Exception as e:
                return f"Error processing DOCX: {e}"

        elif file_type == "text/plain":
            try:
              return uploaded_file.getvalue().decode("utf-8")
            except Exception as e:
                return f"Error processing TXT: {e}"

        else:
            return "❌ Unsupported file format. Please upload a PDF, DOCX, or TXT file."

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
    if file_text and not file_text.startswith("Error"):
        st.success("✅ File uploaded successfully!")
        st.text_area("Extracted Text (Preview):", file_text[:1000], height=150)
    elif file_text:
        st.error(file_text)

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

# Debugging section to list models.
try:
    models = genai.list_models()
    st.sidebar.write("Available Models:")
    for model in models:
        st.sidebar.write(f"- {model.name}")

except Exception as e:
    st.sidebar.error(f"Error listing models: {e}")
