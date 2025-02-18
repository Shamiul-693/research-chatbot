import streamlit as st
import google.generativeai as genai

# Set up API key (Replace with your actual API key)
genai.configure(api_key="AIzaSyCT-bvj0EJke7lBkGZRbeWF31v9XOSAHLg")

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI with Chat History
st.set_page_config(page_title="AI Research Chatbot", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.title("🔍 Research Assistant Chatbot")
st.sidebar.write("💡Powered by Shamiul Islam https://www.facebook.com/samiulislam.693 ")
st.sidebar.write("📝 Ask research-related questions and get instant AI-generated insights.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Messages
st.title("🚀 AI Research Assistant SamBotChat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Type your question here...")
if user_input:
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    with st.spinner("Thinking... 🤖💭"):
        ai_response = chat_with_gemini(user_input)
    
    # Append AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
