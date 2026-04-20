from services.api_client import post

def send_emails(meeting_id):
    return post(f"/emails/send/{meeting_id}", {})

