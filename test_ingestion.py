from dotenv import load_dotenv
load_dotenv()

from app.core.pipeline import build_pipeline, query_pipeline

# Step 1 - Ingest document
build_pipeline("data/sample.txt")

# Step 2 - Query it
results = query_pipeline("What is RAG?", k=2)

# Step 3 - Print results
for i, doc in enumerate(results):
    print(f"--- Chunk {i+1} ---")
    print(doc.page_content)
    print()