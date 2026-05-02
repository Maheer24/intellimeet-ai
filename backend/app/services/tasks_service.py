from app.db.supabase_client import supabase
from datetime import date
from uuid import UUID


class TaskService:
    def save_task(
        self,
        meeting_id: UUID,
        task: str,
        owner: str,
        due_date: date,
        status: str = "Pending",
    ):
        try:
            response = (
                supabase.table("tasks")
                .insert(
                    {
                        "meeting_id": str(meeting_id),
                        "task": task,
                        "owner": owner,
                        "due_date": due_date if due_date else None,
                        "status": status,
                    }
                )
                .execute()
            )

            return response.data

        except Exception as e:
            raise RuntimeError(f"Failed to create task: {e}")
        
    
        
    def get_task_by_meeting(self, meeting_id: UUID):
        try:
            response = (
                supabase.table("tasks")
                .select("id", "task", "owner", "due_date", "status")
                .eq("meeting_id", str(meeting_id))
                .execute()
            )
            return response.data

        except Exception as e:
            raise RuntimeError(f"Failed to fetch task: {e}")

    def update_task_status(self, task_id: UUID, status: str):
        try:
            response = (
                supabase.table("tasks")
                .update({"status": status})
                .eq("id", str(task_id))
                .execute()
            )
            return response

        except Exception as e:
            raise RuntimeError(f"Failed to fetch task: {e}")
