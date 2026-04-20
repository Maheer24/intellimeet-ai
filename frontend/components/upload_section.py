import streamlit as st
from services.meeting_api import upload_meeting
from services.email_api import send_emails

def upload_section():
    st.subheader("Upload Transcript")

    file = st.file_uploader("Upload .txt file")

    if st.button("Generate Summary"):
        if file:
            with st.spinner("Processing transcript..."):
                res = upload_meeting(file)

                st.session_state.meeting_id = res["meeting_id"]
                st.session_state.summary = res["summary"]

    if "summary" in st.session_state:
        st.text_area("Summary", st.session_state.summary, height=200)

        if st.button("Send Emails"):
            with st.spinner("Sending emails..."):
                send_emails(st.session_state.meeting_id)
                st.success("Emails sent!")