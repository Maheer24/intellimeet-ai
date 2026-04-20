
import streamlit as st
from services.task_api import get_tasks, update_task

def task_management():
    st.subheader("Tasks")

    if "meeting_id" not in st.session_state:
        st.info("Upload a meeting first")
        return

    tasks = get_tasks(st.session_state.meeting_id)

    for task in tasks:
        col1, col2, col3, col4 = st.columns([3,2,2,2])

        col1.write(task["task"])
        col2.write(task["owner"])
        col3.write(task["status"])

        if col4.button("Complete", key=task["id"]):
            update_task(task["id"], "Completed")
            st.rerun()