from backend.app.db.supabase_client import supabase
from uuid import UUID


class MeetingService:

    def save_meeting(self, summary: str, transcript: str, title: str):

        try:
            response = (
                supabase.table("meetings")
                .insert({"transcript": transcript, "summary": summary, "title": title})
                .execute()
            )
            return response.data[0]["id"]

        except Exception as e:
            raise RuntimeError(f"Faled to save meeting: {e}")

    def get_meeting_summary(self, meeting_id: UUID):
        try:
            response = (
                supabase.table("meetings")
                .select("summary")
                .eq("id", str(meeting_id))
                .single()
                .execute()
            )

            return response

        except Exception as e:
            raise RuntimeError(f"Faled to fetch meeting: {e}")

    def get_all_meetings(self):
        try:
            response = (
                supabase.table("meetings")
                .select("id","summary", "transcript", "title")
                .execute()
            )
            return response

        except Exception as e:
            raise RuntimeError(f"Faled to fetch meetings: {e}")
