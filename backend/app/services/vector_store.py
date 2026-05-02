from pinecone import Pinecone, ServerlessSpec
import uuid
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_api = os.getenv("PINECONE_API_KEY")

class PineconeService:
    def __init__(self, index_name: str = "intellimeet-index", dimension: int = 384):
        self.index_name = index_name
        self.pc = Pinecone(api_key=pinecone_api)
        self.dimension = dimension

        self.index = self._create_index()

    def _create_index(self):
        try:
            if not self.pc.has_index(self.index_name):
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            return self.pc.Index(self.index_name)
        
        except Exception as e:
            raise RuntimeError(f"Error creating index: {e}")

    def upsert_embeddings(self, embeddings: list[list[float]], chunks: list[str], meeting_id:UUID):
        try:
            upsert_data = []

            for index, (embedding,chunk) in enumerate(zip(embeddings, chunks)):
                
                print("Embeddings: ",len(embeddings))
                print("Chunks: ",len(chunks))
                print("Upserting:", len(upsert_data))

                upsert_data.append({
                    "id": str(uuid.uuid4()),
                    # convert numpy array to list
                    "values": embedding,
                    "metadata": {
                        "meeting_id": str(meeting_id),
                        "text": chunk
                    } 
                })

            response = self.index.upsert(vectors = upsert_data)
            return(f"Upsert response: {response}")

        except Exception as e:
            raise RuntimeError(f"Error upserting embeddings: {e}")

    def query(self, query_embedding:str, top_k:int = 3, meeting_id:UUID = None):

        try:
            filter_dict = None

            if meeting_id:
                # $eq: Matches vectors with metadata values that are equal to a specified value. 
                filter_dict = {"meeting_id": {"$eq": str(meeting_id)}}

            response = self.index.query(
                vector = query_embedding,
                top_k = top_k,
                filter = filter_dict,
                include_metadata = True,
            )

            result = [
                {
                    "text": match["metadata"]["text"], 
                    "score": match["score"]
                } 
                
                for match in response["matches"]
            ]
            return result
        
        except Exception as e:
            raise RuntimeError(f"Error querying: {e}")


    def delete_by_meeting(self, meeting_id:UUID):
        try:
            self.index.delete(filter = {"meeting_id": {"$eq": str(meeting_id)}})
        except Exception as e:
            raise RuntimeError(f"Error deleting query: {e}")