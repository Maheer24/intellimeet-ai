from fastapi import FastAPI
from backend.app.routers.email_router import router as email_router
from backend.app.routers.meeting_router import router as meeting_router
from backend.app.routers.task_router import router as task_router
from backend.app.routers.user_router import router as user_router
from backend.app.routers.chat_router import router as chat_router

app = FastAPI()

app.include_router(email_router)
app.include_router(meeting_router)
app.include_router(task_router)
app.include_router(user_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "App running"}
