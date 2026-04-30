import streamlit as st
from services.user_api import add_user, get_users, delete_user, update_user_email

def user_management():
    st.subheader("Users")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add User"):

        res = add_user(name, email)

        if "error" in res:
            st.error("Failed to add user")
        else:
            st.success("User added")


    users = get_users()

    if not isinstance(users, list):
        st.error("Failed to load users")
        st.write(users)
        return
    
    #st.write(users)

    for user in users:
        col1, col2, col3 = st.columns([2,3,2])

        # Column 1: Name
        with col1.container():
            st.markdown("#####")  # spacing
            st.markdown("#####")
            st.write(user["name"])

        # Column 2: Email input
        with col2.container():
            st.markdown("#####")
            new_email = st.text_input(
                label="Email",
                key=user["id"]
            )

        # Column 3: Buttons
        with col3.container():
            st.markdown("#####")
            btn1, btn2 = st.columns(2)

            if btn1.button("Update", key=f"u{user['id']}"):
                res = update_user_email(user["id"], new_email)
                if "error" in res:
                    st.error("Failed to update user email")
                else:
                    st.success("Updated user email")

            if btn2.button("Delete", key=f"d{user['id']}"):
                delete_user(user["id"])
                st.rerun()