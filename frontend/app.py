import streamlit as st

st.set_page_config(layout="wide", page_title="IntelliMeet AI")

st.sidebar.title("IntelliMeet AI")

page = st.sidebar.radio("Navigate", ["Dashboard", "IntelliChat"])

if page == "Dashboard":
    #st.write("Dashboard loaded")
    from pages.dashboard import show_dashboard
    show_dashboard()

elif page == "IntelliChat":
    #st.write("Chat loaded")
    from pages.intellichat import show_chat
    show_chat()