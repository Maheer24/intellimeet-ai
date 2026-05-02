from app.utils.chunker import fixed_size_chunk_with_overlap
from uuid import UUID

class RAGService:
    def __init__(self, embedding_service, pinecone_service, llm_service, task_service, memory_service):
        self.embedding_service = embedding_service
        self.pinecone_service = pinecone_service
        self.llm_service = llm_service
        self.task_service = task_service
        self.memory_service = memory_service

    def ingest_meeting(
        self,
        transcript: str,
        meeting_id: UUID,
        overlap: int = 30,
        chunk_size: int = 200,
    ):
        """Takes meeting transcript as input, creates chunks, then generates embeddings and stores in pinecone"""
        try:
            chunks_list = fixed_size_chunk_with_overlap(transcript, overlap, chunk_size)
            embeddings = self.embedding_service.generate_embeddings(chunks_list)
            self.pinecone_service.upsert_embeddings(
                embeddings, chunks_list, str(meeting_id)
            )
        except Exception as e:
            raise RuntimeError(f"Error ingesting meeting: {e}")

    def retrieve_context(self, query: str, meeting_id: UUID, top_k: int = 3):
        """Retrieves relevant information according to user's query"""
        try:
            query_embedding = self.embedding_service.generate_embeddings([query])[0]
            result = self.pinecone_service.query(query_embedding, top_k, str(meeting_id))

            #covert dict to str
            context_chunks = [item["text"] if isinstance(item, dict) else item for item in result]
            return context_chunks
        
        except Exception as e:
            raise RuntimeError(f"Error retrieving context: {e}")

    def build_prompt(self, query: str, context_chunks: list[str], chat_history: list):
        try:
            # \n".join() takes the list of strings and joins them together into one large string, using the newline character (\n) as the separator.
            history = "\n".join(
                [f"{chat['role']}: {chat['content']}"for chat in chat_history or []]
            ) 

            context = "\n".join(context_chunks)
            prompt = f"""
            You are a helpful meeting assistant. Answer the query using only the context below.

            conversation_history: {history}
            context: {context}
            query: {query}

            Rules:
            - Use conservation history if needed.
            - If no relevant context is present, politely say that this was not mentioned in meeting.
            - Be concise.
            """
            return prompt

        except Exception as e:
            raise RuntimeError(f"Error building prompt: {e}")

    def query(self, user_query: str, meeting_id: UUID,session_id: UUID):
        try:
            chat_history = self.memory_service.retrieve_history(session_id)

            context_chunks = self.retrieve_context(user_query, str(meeting_id))

            prompt = self.build_prompt(user_query, context_chunks, chat_history)

            response = self.llm_service.generate_text(prompt, max_tokens = 300)

            self.memory_service.store_messages(session_id, "user", user_query)
            self.memory_service.store_messages(session_id, "assistant", response)

            return response

        except Exception as e:
            raise RuntimeError(f"Error generating response: {e}")
