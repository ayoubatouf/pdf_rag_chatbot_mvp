from src.groq_client import GroqClient
from src.document_processor import DocumentProcessor
from src.embedding_model import EmbeddingModel
import logging
import os
from src.index_manager import IndexManager


class RAGSystem:
    def __init__(
        self,
        config,
        document_processor: DocumentProcessor,
        embedding_model: EmbeddingModel,
        index_manager: IndexManager,
        groq_client: GroqClient,
    ):
        self.config = config
        self.document_processor = document_processor
        self.embedding_model = embedding_model
        self.index_manager = index_manager
        self.groq_client = groq_client
        self._initialize_system()

    def _initialize_system(self):
        try:
            texts, metadata = self.document_processor.process(
                self.config["data_directory"]
            )
            embeddings = self.embedding_model.encode(texts)
            self.index_manager.create_index(texts, embeddings, metadata)
        except Exception as e:
            logging.error(f"Error initializing RAG system: {str(e)}")
            raise

    def query(self, user_query, top_k=3):
        try:
            query_embedding = self.embedding_model.encode([user_query])[0]
            results = self.index_manager.retrieve_documents(query_embedding, top_k)

            context_lines = []
            for text, meta in results:
                if not meta:
                    continue
                pages = list(set(m[1] for m in meta))
                filename = os.path.basename(meta[0][0]) if meta else "unknown"
                context_lines.append(
                    f"(Pages {', '.join(map(str, sorted(pages)))} in {filename}): {text}"
                )

            return self.groq_client.generate_answer(
                user_query, "\n".join(context_lines)
            )
        except Exception as e:
            logging.error(f"Error processing query: {str(e)}")
            raise

    def run(self):
        logging.info("RAG System initialized. Type 'exit' to quit.")
        while True:
            query = input("\nEnter your query: ")
            if query.lower() == "exit":
                break
            try:
                answer = self.query(query)
                print(f"\nAnswer: {answer}")
            except Exception as e:
                logging.error(f"Error processing query: {str(e)}")
                print(f"\nError processing query: {str(e)}")
