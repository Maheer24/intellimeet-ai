from fastapi import APIRouter
from app.services.user_service import UserService
from uuid import UUID
from fastapi import Body

user_service = UserService()
router = APIRouter(prefix="/users")

@router.post("/")
def add_user(name:str = Body(...), email:str = Body(...)):
    return user_service.add_user(name,email)

@router.delete("/{user_id}")
def delete_user(user_id:UUID):
    return user_service.remove_user(user_id)
    

@router.patch("/{user_id}")
def update_email(user_id: UUID, email: str = Body(..., embed=True)):
    return user_service.update_user_email(user_id, email)

@router.get("/")
def get_users():
    return user_service.get_all_users()
    