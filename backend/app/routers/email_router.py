from fastapi import APIRouter
from backend.app.services.email_service import EmailService
from backend.app.services.llm_service import LLMService
from backend.app.services.meeting_service import MeetingService
from backend.app.services.tasks_service import TaskService
from backend.app.services.user_service import UserService
from uuid import UUID
from dotenv import load_dotenv
import os
load_dotenv()
groq_api = os.getenv("GROQ_API_KEY")

system_prompt = """
You are a meeting assistant for a company. You are detail oriented and professional.
    """
llm_service = LLMService(system_message=system_prompt)

meeting_service = MeetingService()
task_service = TaskService()
user_service = UserService()
email_service = EmailService(llm_service, meeting_service, task_service, user_service)

router = APIRouter(prefix="/emails")

@router.post("/draft/{meeting_id}")
def draft_email(meeting_id: UUID):
    email = email_service.draft_email(meeting_id=meeting_id)

    email_subject = email["subject"]
    email_body = email["email_body"]

    return {"email_subject": email_subject, "email_body": email_body}


@router.post("/save/{meeting_id}")
def save_email(meeting_id: UUID, subject: str, body: str, recipient: str):
    response = email_service.save_email(meeting_id, body, recipient, subject)
    return {"email_id": response}

@router.post("/send/{meeting_id}")
def send_emails(meeting_id:UUID):
    """Drafts, saves, sends email then also updates status"""
    email_service.send_bulk_emails(meeting_id)

    return {"message": "Emails sent successfully"}

# @router.post("/send/{email_id}")
# def send_email(email_id: UUID):
#     email_data = email_service.get_email_by_id(email_id)

#     email_service.send_email(
#         recipient_email=email_data["recipient"],
#         body=email_data["email_body"],
#         subject=email_data["subject"],
#     )
#     email_service.update_status(email_id)

#     return {"message": "Email sent"}


@router.get("/{meeting_id}")
def get_email(meeting_id: UUID):
    email_data = email_service.get_email_by_meeting(meeting_id)

    return email_data

    # json_list = json.loads(email)
    # for object in json_list:
    #     email_body = object["email_body"]
    #     subject = object["subject"]
    #     recipient = object["recipient"]
    #     status = object["status"]
    #     created_at = object["created_at"]
    # return json_list
