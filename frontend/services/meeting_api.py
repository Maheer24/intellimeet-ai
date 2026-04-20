from services.api_client import post, get

def upload_meeting(file):
    files = {"file": file}
    return post("/meetings/upload", files=files)

def get_all_meetings():
    return get("/meetings/")