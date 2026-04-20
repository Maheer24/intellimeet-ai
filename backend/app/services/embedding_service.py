from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

class EmbeddingService:
    """
    Generates embeddings using text chunks for Sentence Transformers
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device:str = "cpu"):
        try:
            self.model = SentenceTransformer(model_name, device = device)
        except Exception as e:
            raise RuntimeError(f"Error initializing model: {e}")

    def generate_embeddings(self, chunks_list: list[str]) -> list[list[float]]:
        try:
            embeddings = self.model.encode(chunks_list,batch_size=16, convert_to_numpy=True, show_progress_bar=True)
            embeddings = normalize(embeddings)
            return embeddings
        
        except Exception as e:
            raise RuntimeError(f"Error generating embeddings: {e}")
