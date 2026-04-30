from services.api_client import get, patch

def get_tasks(meeting_id):
    return get(f"/tasks/{meeting_id}")

def update_task(task_id):
    return patch(f"/tasks/{task_id}")