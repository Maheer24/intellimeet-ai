import streamlit as st
from services.chat_api import send_query
from utils.session import get_session_id

def show_chat():
    st.title("IntelliChat ⚆_⚆")

    session_id = get_session_id()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    # Chat input at bottom
    user_input = st.chat_input("Ask something about your meeting...")

    if user_input:
        meeting_id = st.session_state.get("meeting_id")

        if not meeting_id:
            st.warning("Please upload a meeting first")
            return

        # Show user message instantly
        st.session_state.chat_history.append(("user", user_input))

        with st.chat_message("user"):
            st.markdown(user_input)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_query(user_input, meeting_id, session_id)
                st.markdown(response)

        # Save assistant response
        st.session_state.chat_history.append(("assistant", response))