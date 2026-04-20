import streamlit as st
from services.chat_api import send_query
from utils.session import get_session_id

def show_chat():
    st.title("IntelliChat ⚆_⚆")

    session_id = get_session_id()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask something...", key="chat_input")

    if st.button("Send"):
        if user_input:
            meeting_id = st.session_state.get("meeting_id")

            if not meeting_id:
                st.warning("Please upload a meeting first")
                return

            with st.spinner("Thinking..."):
                response = send_query(user_input, meeting_id, session_id)

                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("assistant", response))

            st.session_state.chat_input = "" 

    # Display chat
    for role, msg in reversed(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Assistant:** {msg}")