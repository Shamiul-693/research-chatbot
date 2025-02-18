import streamlit as st
import google.generativeai as genai

# Set up API key
genai.configure(api_key="AIzaSyCT-bvj0EJke7lBkGZRbeWF31v9XOSAHLg")

# Function to chat with Gemini AI
def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("🚀 Free AI Research Assistant")
st.write("Ask any research-related question below:")

user_input = st.text_input("Your question:")
if user_input:
    response = chat_with_gemini(user_input)
    st.write("### 🤖 AI Response:")
    st.write(response)
