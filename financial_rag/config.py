import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CHROMA_DB_PATH = "financial_rag/data/chroma_db"
EMBED_MODEL_NAME = 'all-MiniLM-L6-v2'
LLM_MODEL = "deepseek-r1:14b"
EXPERT_PROMPT_PATH = "financial_rag/Expert_Prompt"
