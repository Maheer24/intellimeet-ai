import streamlit as st
from services.meeting_api import get_all_meetings
from services.task_api import get_tasks
from services.user_api import get_users

def show_metrics():
    try:
        meetings = get_all_meetings()
        users = get_users()

        total_meetings = len(meetings)
        total_users = len(users)

        # Count pending tasks across meetings
        pending_tasks = 0

        for meeting in meetings:
            meeting_id = meeting["id"]
            tasks = get_tasks(meeting_id)

            for task in tasks:
                if task["status"] == "Pending":
                    pending_tasks += 1

        col1, col2, col3 = st.columns(3)

        col1.metric("📅 Total Meetings", total_meetings)
        col2.metric("📝 Pending Tasks", pending_tasks)
        col3.metric("👥 Users", total_users)

    except Exception as e:
        st.error(f"Error loading metrics: {e}")