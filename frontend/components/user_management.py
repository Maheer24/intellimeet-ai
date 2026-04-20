import streamlit as st
from services.user_api import add_user, get_users, delete_user, update_user_email

def user_management():
    st.subheader("Users")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add User"):
        add_user(name, email)
        st.success("User added")

    users = get_users()

    if not isinstance(users, list):
        st.error("Failed to load users")
        st.write(users)
        return
    
    #st.write(users)

    for user in users:
        col1, col2, col3 = st.columns(3)

        col1.write(user["name"])
        new_email = col2.text_input("Update Email", key=user["id"])

        if col2.button("Update", key=f"u{user['id']}"):
            update_user_email(user["id"], new_email)

        if col3.button("Delete", key=f"d{user['id']}"):
            delete_user(user["id"])
            st.rerun()