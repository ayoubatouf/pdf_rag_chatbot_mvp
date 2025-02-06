from src.index_manager import IndexManager
import os
import logging
import faiss
import pickle


class FAISSIndexManager(IndexManager):
    def __init__(self, index_path, metadata_path, documents_path):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.documents_path = documents_path
        self.index = None
        self.metadata = None
        self.documents = None

    def index_exists(self):
        return (
            os.path.exists(self.index_path)
            and os.path.exists(self.metadata_path)
            and os.path.exists(self.documents_path)
        )

    def create_index(self, documents, embeddings, metadata):
        try:
            dimension = embeddings.shape[1]
            nlist = max(1, min(4, len(documents)))

            quantizer = faiss.IndexFlatL2(dimension)
            self.index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
            self.index.train(embeddings)
            self.index.add(embeddings)

            self.documents = documents
            self.metadata = metadata
            self.save_index()
        except Exception as e:
            logging.error(f"Error creating FAISS index: {str(e)}")
            raise

    def save_index(self):
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, "wb") as f:
                pickle.dump(self.metadata, f)
            with open(self.documents_path, "wb") as f:
                pickle.dump(self.documents, f)
        except Exception as e:
            logging.error(f"Error saving FAISS index: {str(e)}")
            raise

    def load_index(self):
        try:
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
            with open(self.documents_path, "rb") as f:
                self.documents = pickle.load(f)
        except Exception as e:
            logging.error(f"Error loading FAISS index: {str(e)}")
            raise

    def retrieve_documents(self, query_embedding, top_k=3):
        try:
            _, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
            return [
                (self.documents[i], self.metadata[i])
                for i in indices[0]
                if i < len(self.documents)
            ]
        except Exception as e:
            logging.error(f"Error retrieving documents from FAISS index: {str(e)}")
            raise
