import streamlit as st
from components.upload_section import upload_section
from components.user_management import user_management
from components.task_management import task_management
from components.metrics_card import show_metrics
def show_dashboard():
    st.title("📊 Dashboard")

    show_metrics()
    st.divider()
    
    upload_section()
    st.divider()

    user_management()
    st.divider()

    task_management()