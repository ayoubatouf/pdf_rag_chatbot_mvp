from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.faiss_index_manager import FAISSIndexManager
from src.groq_client import GroqClient
from src.pdf_document_processor import PDFDocumentProcessor
from src.rag_system import RAGSystem
from src.sentence_embedding_model import SentenceEmbeddingModel
from src.utils import load_config, setup_logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


setup_logging()
config = load_config()
document_processor = PDFDocumentProcessor(
    chunk_size=config["chunk_size"], chunk_overlap=config["chunk_overlap"]
)
embedding_model = SentenceEmbeddingModel(model_name=config["embedding_model"])
index_manager = FAISSIndexManager(
    index_path=config["index_path"],
    metadata_path=config["metadata_path"],
    documents_path=config["documents_path"],
)
groq_client = GroqClient(
    api_key=config["groq_api_key"], model_name=config["groq_model"]
)

rag_system = RAGSystem(
    config, document_processor, embedding_model, index_manager, groq_client
)


@app.post("/chat/")
async def chat(request: QueryRequest):
    try:
        answer = rag_system.query(request.query)
        return {"response": answer}
    except Exception as e:
        return {"error": f"Error processing query: {str(e)}"}
