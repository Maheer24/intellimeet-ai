from fastapi import APIRouter, Body
from uuid import UUID
from backend.app.services.rag_service import RAGService
from backend.app.services.vector_store import PineconeService
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.vector_store import PineconeService
from backend.app.services.llm_service import LLMService
from backend.app.services.tasks_service import TaskService
from backend.app.services.memory_service import MemoryService

embedding_service = EmbeddingService()
pinecone_service = PineconeService()
llm_service = LLMService()
task_service = TaskService()
memory_service = MemoryService()

rag_service = RAGService(embedding_service, pinecone_service, llm_service, task_service, memory_service)

router = APIRouter(prefix="/chat")

@router.post("/")
def post_query(user_query:str = Body(...), meeting_id:UUID = Body(...), session_id:UUID = Body(...)):
    response = rag_service.query(user_query, meeting_id, str(session_id))
    return {"response": response}

@router.get("/memory/{session_id}")
def get_conversation_memory(session_id: UUID):
    history = memory_service.retrieve_history(str(session_id))
    return{"history": history}

@router.delete("/memory/{session_id}")
def delete_conversation_memory(session_id: UUID):
    return memory_service.delete_history(str(session_id))
    



