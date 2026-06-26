from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_embedding_model():
    """
    Returns Gemini embedding model.
    This converts text → vectors.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    print("[Embeddings] Gemini embedding model loaded")
    return embeddings