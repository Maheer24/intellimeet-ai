from services.api_client import post

def send_query(user_query, meeting_id, session_id):
    data = {
        "user_query": user_query,
        "meeting_id": str(meeting_id),
        "session_id": str(session_id)
    }
    return post("/chat/", data)["response"]