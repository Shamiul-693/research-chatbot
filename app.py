# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vg8mavbCtsWMAs4IWTaLv6kg2nv_Mekf
"""

import streamlit as st
from transformers import pipeline

# Load a free Hugging Face model (small but works well)
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

def chat_with_ai(prompt):
    """Generate chatbot response using Hugging Face's model"""
    response = chatbot(prompt, max_length=100, pad_token_id=50256)
    return response[0]["generated_text"]

# Streamlit UI
st.title("🆓 Free AI Research Assistant Chatbot")
st.write("Ask any research-related question below:")

# User input
user_input = st.text_input("Your question:")
if user_input:
    response = chat_with_ai(user_input)
    st.write("### 🤖 AI Response:")
    st.write(response)