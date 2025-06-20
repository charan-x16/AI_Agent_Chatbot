import streamlit as st
import requests

st.set_page_config(page_title="AI Agent Chatbot", layout="centered")

st.title("AI Agent Chatbot")
st.markdown("Chat with powerful LLMs like Groq and Gemini with optional web search!")

with st.sidebar:
    st.header("Agent Configuration")

    model_provider = st.selectbox("Model Provider", ["Groq", "Gemini"])

    model_name = st.selectbox("Model Name", ["llama3-70b-8192", "gemini-2.5-flash"])

    system_prompt = st.text_area("System Prompt",
                                 value="Act as an AI Chatbot who is smart and friendly",
                                 height=100)
    
    allow_search = st.checkbox("Enable Web Search Tool", value=False)


# Session State for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("User"):
            st.markdown(msg)

    else:
        with st.chat_message("AI"):
            st.markdown(msg)


# Handles User Query
user_query = st.chat_input("Type your message......")

if user_query:
    # Display user message 
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append(("user", user_query))

    # Send request to FastAPI backend
    with st.chat_message("AI"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "model_name": model_name,
                    "model_provider": model_provider,
                    "system_prompt": system_prompt,
                    "messages": [user_query],
                    "allow_search": allow_search       
                }

                res = requests.post("http://localhost:8000/chat", json=payload)
                response = res.json()
                st.markdown(response)
                st.session_state.chat_history.append(("AI", response))
            except Exception as e:
                st.error(f"Error: {e}")