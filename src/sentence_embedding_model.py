from src.embedding_model import EmbeddingModel
from sentence_transformers import SentenceTransformer
import logging


class SentenceEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        try:
            return self.model.encode(texts, convert_to_numpy=True).astype("float32")
        except Exception as e:
            logging.error(f"Error encoding texts with model {self.model}: {str(e)}")
            raise
