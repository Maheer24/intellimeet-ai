from uuid import UUID

class MemoryService:
    """
    Format of storing session history:
    {"session_1": 
        [
            {"role": role, "content": content}, 
            {"role": role, "content": content}
        ],
    "session_2": 
        [
            {"role": role, "content": content}, 
            {"role": role, "content": content}
        ],
    }
    """

    def __init__(self):
        self.store = {}
        

    def store_messages(self, session_id: UUID, role:str, content:str):
        try:
            session_id = str(session_id)

            if session_id not in self.store:
                self.store[session_id] = []
            
            self.store[session_id].append(
                {
                    "role": role,
                    "content": content
                }
            )
        except Exception as e:
            raise RuntimeError(f"Error storing history: {e}")


    def retrieve_history(self, session_id: UUID, limit:int = 5):
        try:
            session_id = str(session_id)
            history = self.store.get(session_id, [])
            return history[-limit:]

        except Exception as e:
            raise RuntimeError(f"Error retrieving history: {e}")

    def delete_history(self, session_id:UUID):
        try:
            session_id = str(session_id)
            self.store.pop(session_id, None)
            return {
                "message": f"History deleted of session:{session_id}"
            }
        except Exception as e:
            raise RuntimeError(f"Error deleting history: {e}")
    