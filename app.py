import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot - Local LLM", layout="centered")

st.title("🤖 Intelligent AI Chatbot (Local LLM)")
st.caption("Powered by TinyLlama via Ollama (Runs Fully Offline)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
prompt = st.chat_input("Type your question here...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Structured professional prompt
    structured_prompt = f"""
You are a professional AI assistant.
Answer clearly, briefly, and directly.
Avoid unnecessary explanations.
Keep responses under 6 sentences.

User Question:
{prompt}

Answer:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": structured_prompt,
                "stream": False
            },
            timeout=60
        )

        result = response.json()
        bot_reply = result.get("response", "Sorry, I couldn't generate a response.")

    except Exception as e:
        bot_reply = "Error connecting to the local AI model. Please ensure Ollama is running."

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )