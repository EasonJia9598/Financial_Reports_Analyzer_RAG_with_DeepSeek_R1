import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from financial_rag.backend.vector_db import VectorDatabase
from financial_rag.models.models import EmbeddingModel

class SearchEngine:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.embed_model = EmbeddingModel()

    def get_page_content(self, url, max_length=300):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
            content = " ".join(paragraphs)
            return content[:max_length] + "..." if len(content) > max_length else content
        except:
            return "Content unavailable"

    def search(self, query, num_results=5):
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=num_results)
            return [{"title": item["title"], "url": item["href"], "snippet": self.get_page_content(item["href"])} for item in results]

    def update_web_results(self, query, num_results=5):
        """Fetches web search results, generates embeddings, and updates the vector database."""
        
        # Perform search
        results = self.search(query, num_results)
        if not results:
            return []

        # Format the documents properly
        docs = [f"Title: {res['title']}\nSummary: {res['snippet']}" for res in results]

        # Generate embeddings for the documents
        embeddings = self.embed_model.encode(docs)

        # Generate unique IDs for each document
        ids = [f"web_{i}" for i in range(len(docs))]

        # Prepare metadata for each document
        metadatas = [
            {"source": "web", "url": res["url"], "title": res["title"]}
            for res in results
        ]

        # Add documents to the vector database
        self.vector_db.add_documents(ids, embeddings, docs, metadatas)

        return results
    
