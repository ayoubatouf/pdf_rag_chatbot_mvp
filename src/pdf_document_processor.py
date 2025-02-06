from src.document_processor import DocumentProcessor
import logging
import fitz
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFDocumentProcessor(DocumentProcessor):
    def __init__(self, chunk_size=5000, chunk_overlap=100, log_file="chunks_log.txt"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        self.log_file = log_file

    @staticmethod
    def extract_text_with_page_metadata(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            full_text = []
            page_metadata = []
            for page_num, page in enumerate(doc):
                text = page.get_text("text").strip()
                if text:
                    full_text.append(text)
                    page_metadata.extend([(pdf_path, page_num + 1)] * len(text))
                    full_text.append("\n")
            return "".join(full_text), page_metadata
        except Exception as e:
            logging.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise

    def process(self, directory_path):
        combined_texts = []
        combined_metadata = []
        chunk_count = 0

        try:
            with open(self.log_file, "w") as log:
                for filename in os.listdir(directory_path):
                    if not filename.endswith(".pdf"):
                        continue

                    file_path = os.path.join(directory_path, filename)
                    try:
                        full_text, page_metadata = self.extract_text_with_page_metadata(
                            file_path
                        )
                        chunks = self.splitter.split_text(full_text)
                        chunk_count += len(chunks)

                        for chunk in chunks:
                            start_idx = full_text.find(chunk)
                            end_idx = start_idx + len(chunk)
                            relevant_metadata = self._get_chunk_metadata(
                                page_metadata, start_idx, end_idx
                            )

                            combined_texts.append(chunk)
                            combined_metadata.append(relevant_metadata)

                            log.write(f"--- Chunk from {filename} ---\n")
                            log.write(f"Pages: {[m[1] for m in relevant_metadata]}\n")
                            log.write(chunk + "\n\n")
                    except Exception as e:
                        logging.error(f"Error processing file {filename}: {str(e)}")

            logging.info(f"Total chunks: {chunk_count}")
            return combined_texts, combined_metadata
        except Exception as e:
            logging.error(f"Error processing directory {directory_path}: {str(e)}")
            raise

    def _get_chunk_metadata(self, page_metadata, start, end):
        unique_pages = set()
        end_idx = min(end, len(page_metadata))
        for idx in range(start, end_idx):
            unique_pages.add(page_metadata[idx])
        return sorted(unique_pages, key=lambda x: x[1])
