from services.api_client import get, post

def get_tasks(meeting_id):
    return get(f"/tasks/{meeting_id}")

def update_task(task_id, status):
    return post(f"/tasks/update/{task_id}", {"status": status})