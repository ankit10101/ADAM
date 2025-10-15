"""
ADAM (AI-Driven Analytics Manager) Streamlit App

This Streamlit application provides a chat-based interface for automating digital analytics tasks,
leveraging AWS Bedrock AgentCore for intelligent responses. It features session-based chat memory,
sidebar controls, and integration with GTM, GA4, and Selenium-powered browser automation.

Key Features:
- Chat interface for user queries and assistant responses.
- AWS Bedrock AgentCore integration for AI-powered analytics automation.
- Sidebar with app description, clear chat button, and credits.
- Session state management for chat history.
- Responsive UI with loading spinners and markdown rendering.
"""

import streamlit as st
import boto3
import json

client = boto3.client("bedrock-agentcore", region_name="ap-south-1")

# Streamlit chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------------------
# Streamlit Chat Interface
# ----------------------------------------------------------------

with st.sidebar:
    st.write(
        "*Analytics Made Simple — One Question at a Time. Powered by AWS Bedrock AgentCore*"
    )

    st.caption(
        """**  ADAM (AI-Driven Analytics Manager) — Your intelligent partner for automating the entire digital analytics lifecycle 
               with mastery in GTM, GA4, and Selenium-powered browser automation.**
        """
    )

    st.divider()

    # ✅ Clear Chat Button
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "<p style = 'text-align:center'>Made with ❤️</p>",
        unsafe_allow_html=True,
    )

st.set_page_config(initial_sidebar_state="expanded", layout="wide")

st.title("ADAM 🤖: :red[A]I-:red[D]riven :red[A]nalytics Lifecycle :red[M]anagement")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("How may I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Working on it..."):
            payload = json.dumps({"prompt": user_input})

            response = client.invoke_agent_runtime(
                agentRuntimeArn="arn:aws:bedrock-agentcore:ap-south-1:501931553097:runtime/hosted_agent_xvgwz-X0sl152L4n",
                runtimeSessionId="dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt",  # Must be 33+ chars
                payload=payload,
                qualifier="DEFAULT",  # Optional
            )

            response_body = response["response"].read()
            response_data = json.loads(response_body)["result"]

            st.markdown(response_data)

        st.session_state.messages.append(
            {"role": "assistant", "content": response_data}
        )
