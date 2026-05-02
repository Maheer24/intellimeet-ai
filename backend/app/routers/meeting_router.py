from fastapi import UploadFile, File, APIRouter
from app.services.meeting_service import MeetingService
from app.services.llm_service import LLMService
from app.services.meeting_service import MeetingService
from app.services.tasks_service import TaskService
from app.services.rag_service import RAGService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import PineconeService
from app.services.memory_service import MemoryService
from uuid import UUID
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
groq_api = os.getenv("GROQ_API_KEY")

router = APIRouter(prefix="/meetings")

system_prompt = """
You are a meeting assistant for a software company. You are detail oriented and professional.
    """
llm_service = LLMService(api_key=groq_api, model_id="llama-3.3-70b-versatile", system_message=system_prompt)
meeting_service = MeetingService()
task_service = TaskService()
embedding_service = EmbeddingService()
pinecone_service = PineconeService()
memory_service = MemoryService()

rag_service = RAGService(embedding_service, pinecone_service, llm_service, task_service, memory_service)

@router.post("/upload")
async def upload_meeting_transcript(file: UploadFile = File(...)):
    content_bytes = await file.read()
    transcript = content_bytes.decode("utf-8")

    title = file.filename

    summary = llm_service.generate_summary(transcript, 1024)
    tasks = llm_service.extract_tasks(transcript, 1024)

    meeting_id = meeting_service.save_meeting(summary, transcript, title)

    print("Calling Ingest Meeting")
    rag_service.ingest_meeting(transcript, meeting_id, 30, 200)
    #json_list = json.loads(tasks)

    for task_obj in tasks:
        task = task_obj["task"]
        owner = task_obj["owner"]
        due_date = task_obj["due_date"]
        status = task_obj["status"]

        task_service.save_task(meeting_id, task, owner, due_date, status)

    return {"meeting_id": meeting_id, "summary": summary, "tasks": tasks}



@router.get("/")
def get_all_meetings():
    response = meeting_service.get_all_meetings()
    return response.data


@router.get("/{meeting_id}")
def get_meeting_summary(meeting_id: UUID):
    response = meeting_service.get_meeting_summary(meeting_id)
    return response.data



