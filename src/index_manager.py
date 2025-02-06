from abc import ABC, abstractmethod


class IndexManager(ABC):
    @abstractmethod
    def index_exists(self):
        pass

    @abstractmethod
    def create_index(self, documents, embeddings, metadata):
        pass

    @abstractmethod
    def retrieve_documents(self, query_embedding, top_k=3):
        pass
