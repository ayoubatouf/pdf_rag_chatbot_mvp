from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    @abstractmethod
    def encode(self, texts):
        pass
