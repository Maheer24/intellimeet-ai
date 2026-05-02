from app.db.supabase_client import supabase
from uuid import UUID


class UserService:
    def add_user(self, name: str, email: str):
        try:
            response = (
                supabase.table("users").insert({"name": name, "email": email}).execute()
            )
            return response.data

        except Exception as e:
            raise RuntimeError(f"Error adding user: {e}")

    def remove_user(self, user_id: UUID):
        try:
            response = supabase.table("users").delete().eq("id", str(user_id)).execute()
            return response.data

        except Exception as e:
            raise RuntimeError(f"Error deleting user: {e}")

    def get_user_by_name(self, name: str):
        try:
            print(f"DEBUG name='{name}' len={len(name)} repr={repr(name)}")
            # user = (
            #     supabase.table("users")
            #     .select("id", "email", "name")
            #     .ilike("name", f"%{name}%")
            #     .execute()
            # )
            users = (
                supabase.table("users")
                .select("id", "email", "name")
                .execute()
            )
            print(f"DEBUG result: {users.data}")
            matched_user = [user for user in users.data if name.lower() in user["name"].lower()]
            if not matched_user:
                raise RuntimeError(f"User not found {name}")

            return matched_user[0]
            # if not user.data:
            #     raise RuntimeError(f"User not found {name}")

            # return user.data[0]

        except Exception as e:
            raise RuntimeError(f"Error retrieving user: {e}")

    def update_user_email(self, user_id: UUID, email: str):
        try:
            response = (
                supabase.table("users")
                .update({"email": email})
                .eq("id", str(user_id))
                .execute()
            )
            return response.data[0]

        except Exception as e:
            raise RuntimeError(f"Error updating user email: {e}")
        
    def get_all_users(self):
        try:
            response = supabase.table("users").select("id","name","email").execute()
            return response.data
        except Exception as e:
            raise RuntimeError(f"Error retrieving user data: {e}")

