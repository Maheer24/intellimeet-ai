import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from uuid import UUID
from backend.app.db.supabase_client import supabase
import json
import pandas as pd

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


class EmailService:
    def __init__(self, llm_service, meeting_service, task_service, user_service):
        self.llm_service = llm_service
        self.meeting_service = meeting_service
        self.task_service = task_service
        self.user_service = user_service

    def draft_email(
        self,  name: str, summary: str, tasks: list, temperature: float = 0.5, max_tokens: int = 1024
    ):

        prompt = f"""
        Write a respectful, concise email.
        The email must:
        - Start with greeting then address the person.
        - Include the meeting summary.
        - Include tasks of that person only in bullet points.

        Person: {name}
        Summary: {summary}
        Tasks: {json.dumps(tasks, indent=2)}

        Format: {{
        "subject": "string",
        "email_body": "string"
        }}
        Rules:
        - Do not use actual line breaks. Use \\n for new lines.
        - Strictly return only valid JSON object.
        - Keys must be exactly 'subject' and 'email_body'.
        - Tasks must be mentioned in bullets including the owner and due date if mentioned.
        - No markdown, no code blocks.
        """

        try:
            response = self.llm_service.generate_text(
                prompt=prompt, temperature=temperature, max_tokens=max_tokens
            )

            try:
                email = json.loads(response)
            except:
                cleaned = response.replace("\n", "\\n")
                email = json.loads(cleaned)

            if "subject" not in email or "email_body" not in email:
                raise RuntimeError("Invalid Email structure returned by LLM")

            return email

        except Exception as e:
            raise RuntimeError(f"Error drafting email: {e}")

    def send_bulk_emails(self, meeting_id: UUID):
        try:
            summary = self.meeting_service.get_meeting_summary(meeting_id)
            tasks = self.task_service.get_task_by_meeting(str(meeting_id))

            grouped_tasks = {}
            for task in tasks:
                owner = task.get("owner")

                if not owner:
                    continue

                owner = owner.strip().lower() 
                
                if owner not in grouped_tasks:
                    grouped_tasks[owner] = []

                grouped_tasks[owner].append(task)

            for owner, task_list in grouped_tasks.items():
                user = self.user_service.get_user_by_name(owner)
                email = user["email"]
                name = user["name"]

                email_draft = self.draft_email(
                    name, summary, task_list
                )

                subject = email_draft["subject"]
                email_body = email_draft["email_body"]

                email_id = self.save_email(meeting_id, email_body, email, subject)

                self.send_email(email, email_body, subject)
                self.update_status(email_id)

        except Exception as e:
            raise RuntimeError(f"Error sending bulk emails: {e}")

    def save_email(
        self,
        meeting_id: UUID,
        email_body: str,
        recipient: str,
        subject: str,
        sent: bool = False,
    ):
        try:
            response = (
                supabase.table("emails")
                .insert(
                    {
                        "recipient": recipient,
                        "email_body": email_body,
                        "meeting_id": str(meeting_id),
                        "subject": subject,
                        "sent": sent,
                    }
                )
                .execute()
            )

            return response.data[0]["id"]

        except Exception as e:
            raise RuntimeError(f"Error saving email: {e}")

    def send_email(self, recipient_email: str, body: str, subject: str):
        try:

            message = MIMEMultipart()
            message["From"] = EMAIL_ADDRESS
            message["To"] = recipient_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(
                    from_addr=EMAIL_ADDRESS,
                    to_addrs=recipient_email,
                    msg=message.as_string(),
                )
                return True

        except Exception as e:
            raise RuntimeError(f"Error sending mail: {e}")

    def update_status(self, email_id: UUID):

        responses = (
            supabase.table("emails")
            .update({"sent": True})
            .eq("id", str(email_id))
            .execute()
        )
        return responses.data

    def get_email_by_id(self, email_id: UUID):
        try:
            email = (
                supabase.table("emails").select("*").eq("id", str(email_id)).execute()
            )
            email_data = email.data[0]
            return email_data

        except Exception as e:
            raise RuntimeError(f"Error retrieving email: {e}")

    def get_email_by_meeting(self, meeting_id: UUID):
        try:
            email = (
                supabase.table("emails")
                .select("*")
                .eq("meeting_id", str(meeting_id))
                .execute()
            )
            email_data = email.data
            return email_data

        except Exception as e:
            raise RuntimeError(f"Error retrieving email: {e}")


# if __name__ == "__main__":
#     recipient = "maheershakil1224@gmail.com"
#     subject = "Test Email"
#     body = "This is a test email"
#     service = EmailService()
#     service.send_email(recipient_email=recipient, subject=subject, body=body)
