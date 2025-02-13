import chromadb
from chromadb.config import Settings
from config import CHROMA_DB_PATH

class VectorDatabase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH, settings=Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection("rag_docs")

    def add_documents(self, ids, embeddings, documents, metadatas):
        self.collection.add(ids=ids, embeddings=embeddings.tolist(), documents=documents, metadatas=metadatas)

    def query_documents(self, query_embedding, num_results=10):
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=num_results,
            include=["documents", "metadatas"]
        )
        return results.get("documents", [[]])[0]  # Ensure it always returns a list
