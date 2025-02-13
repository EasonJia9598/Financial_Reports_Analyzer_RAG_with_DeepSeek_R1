from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from financial_rag.backend.vector_db import VectorDatabase
from financial_rag.models.models import EmbeddingModel
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.embed_model = EmbeddingModel()

    def extract_text(self, file):
        output = StringIO()
        extract_text_to_fp(file, output)
        return output.getvalue()

    def process_pdf(self, uploaded_file):
        if not uploaded_file:
            return "❌ Please upload a PDF file first!"

        existing_ids = self.vector_db.collection.get()["ids"]
        pdf_ids = [doc_id for doc_id in existing_ids if doc_id.startswith("pdf_")]
        if pdf_ids:
            self.vector_db.collection.delete(ids=pdf_ids)

        text = self.extract_text(uploaded_file)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
        chunks = text_splitter.split_text(text)
        embeddings = self.embed_model.encode(chunks)

        ids = [f"pdf_{i}" for i in range(len(chunks))]
        metadatas = [{"source": "pdf"} for _ in chunks]
        self.vector_db.add_documents(ids, embeddings, chunks, metadatas)

        return f"📄 PDF processed and stored {len(chunks)} text chunks", len(chunks)
