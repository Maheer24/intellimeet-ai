from fastapi import APIRouter
from uuid import UUID
from backend.app.services.tasks_service import TaskService

task_service = TaskService()

router = APIRouter(prefix="/tasks")


@router.get("/{meeting_id}")
def get_tasks_by_meeting(meeting_id: UUID):
    tasks = task_service.get_task_by_meeting(meeting_id)
    return tasks


@router.patch("/{task_id}")
def update_task_status(task_id: UUID):
    tasks = task_service.update_task_status(task_id, "Completed")
    return tasks.data
