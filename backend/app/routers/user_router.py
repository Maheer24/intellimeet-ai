from fastapi import APIRouter
from backend.app.services.user_service import UserService
from uuid import UUID

user_service = UserService()
router = APIRouter(prefix="/users")

@router.post("/")
def add_user(name:str, email:str):
    return user_service.add_user(name,email)

@router.delete("/{user_id}")
def delete_user(user_id:UUID):
    return user_service.remove_user(user_id)
    

@router.patch("/")
def update_email(user_id: UUID, email: str):
    return user_service.update_user_email(user_id, email)
    