import streamlit as st
import google.generativeai as genai

# Set up API key (Replace with your actual API key)
genai.configure(api_key="AIzaSyCT-bvj0EJke7lBkGZRbeWF31v9XOSAHLg")

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI with Sidebar
st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.title("🔍 Research Assistant SamBotChat")
st.sidebar.write("💡 **Powered by  Shamiul Islam https://www.facebook.com/samiulislam.693**")
st.sidebar.write("📝 Ask research-related questions and get instant AI-generated insights.")

# Main Title with Styling
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚀 AI Research Assistant</h1>", unsafe_allow_html=True)
st.write("### Ask your research-related question below:")

# Text Input Area
user_input = st.text_area("💬 Your question:", placeholder="Type your question here...", height=150)

# Submit Button
if st.button("Ask AI 🤖"):
    if user_input.strip():
        with st.spinner("Generating response... ⏳"):
            response = chat_with_gemini(user_input)
        st.success("✅ AI Response:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a question before submitting!")

# Footer
st.markdown("<br><hr><p style='text-align: center;'>🔬 AI-Powered Research Assistant | Built with Streamlight by Sami </p>", unsafe_allow_html=True)
