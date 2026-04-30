from services.api_client import post, delete, get, patch

def add_user(name, email):
    return post("/users/", {"name": name, "email": email})

def delete_user(user_id):
    return delete(f"/users/{user_id}")

def update_user_email(user_id, email):
    return patch(f"/users/{user_id}", {"email": email})

def get_users():
    return get("/users/")