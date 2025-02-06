from abc import ABC, abstractmethod


class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, directory_path):
        pass
