from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL


def get_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    print("[Embeddings] HuggingFace embedding model loaded")
    return embeddings