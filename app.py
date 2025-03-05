import streamlit as st
import google.generativeai as genai
import docx  # For DOCX processing
import fitz  # PyMuPDF for PDF processing

# Configure API Key Securely
api_key = st.secrets.get("api_key")
if not api_key:
    st.error("❌ API Key not found. Please configure it in Streamlit secrets.")
else:
    genai.configure(api_key=api_key)


# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text if response.text else "⚠️ AI could not generate a response. Try rephrasing your question!"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Function to generate an image using Gemini
def generate_image(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-vision")  # Gemini vision model
        response = model.generate_content(prompt)
        return response.text if response.text else "⚠️ Image generation failed. Try a different prompt!"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            uploaded_file.seek(0)  # Reset file pointer
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = "\n".join([page.get_text("text") for page in doc])

        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            uploaded_file.seek(0)  # Reset file pointer
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            return "❌ Unsupported file format. Please upload a PDF or DOCX file."

        # **Optimize by truncating long texts**
        max_chars = 5000  # Limit text to first 5000 characters for AI prompt
        return text[:max_chars] + ("\n...\n⚠️ Document truncated for processing!" if len(text) > max_chars else "")


# Streamlit UI with Chat History
st.set_page_config(page_title="AI Research Chatbot", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.title("🔍 Research Assistant Chatbot")
st.sidebar.write("💡 Powered by [Shamiul Islam](https://www.facebook.com/samiulislam.693)")
st.sidebar.write("📄 Upload a research document and ask AI about it.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# **Show chat history in sidebar**
st.sidebar.subheader("🗂️ Chat History")
for message in st.session_state.messages:
    role = "👤 You" if message["role"] == "user" else "🤖 AI"
    st.sidebar.text(f"{role}: {message['content'][:50]}...")  # Show short preview of messages

# Add a "Clear Chat" button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display Chat Messages
st.title("🚀 AI Research Assistant - SamBotChat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload your research paper (PDF, DOCX)", type=["pdf", "docx"])
file_text = ""

if uploaded_file:
    file_text = extract_text_from_file(uploaded_file)
    if file_text:
        st.success("✅ File uploaded successfully!")
        st.text_area("Extracted Text (Preview):", file_text[:1000], height=150)

# **User Input Section**
user_input = st.chat_input("Type your question here...")

if user_input:
    full_prompt = f"Document Content:\n{file_text}\n\nUser Question:\n{user_input}" if file_text else user_input

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(f"**You:** {user_input}")

    # AI Response Placeholder
    with st.spinner("Thinking... 🤖💭"):
        ai_response = chat_with_gemini(full_prompt)

    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Display AI Response with better formatting
    with st.chat_message("assistant"):
        st.markdown(f"**AI:**\n\n{ai_response}")

    # Auto-scroll to the latest message
    st.experimental_rerun()

# **Image Generation Section**
st.sidebar.subheader("🎨 Generate an AI Image")
image_prompt = st.sidebar.text_input("Enter an image description:")
if st.sidebar.button("🖼️ Generate Image"):
    if image_prompt:
        with st.spinner("Creating image... 🎨"):
            generated_image = generate_image(image_prompt)
            st.sidebar.image(generated_image, caption="Generated Image", use_column_width=True)
    else:
        st.sidebar.error("❌ Please enter a prompt to generate an image.")
