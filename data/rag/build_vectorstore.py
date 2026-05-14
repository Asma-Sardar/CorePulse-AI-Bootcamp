import json
import chromadb
from chromadb.utils import embedding_functions

# Load knowledge base
kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge_base.json")
with open(kb_path, "r") as f:
    protocols = json.load(f)

# Setup ChromaDB
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "vectorstore"))

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create or reset collection
try:
    client.delete_collection("corepulse_protocols")
except:
    pass

collection = client.create_collection(
    name="corepulse_protocols",
    embedding_function=embedding_fn
)

documents = []
metadatas = []
ids = []

for p in protocols:
    actions_text = " ".join(p["actions"])
    sources_text = " | ".join(p.get("sources", []))
    doc = f"{p['title']}. {p['protocol']} Actions: {actions_text}"

    documents.append(doc)
    metadatas.append({
        "id": p["id"],
        "category": p["category"],
        "readiness_range": p["readiness_range"],
        "workout_type": p["workout_type"],
        "experience_level": p["experience_level"],
        "title": p["title"],
        "return_to_training": p["return_to_training"],
        "warning": p["warning"],
        "actions": json.dumps(p["actions"]),
        "sources": sources_text
    })
    ids.append(p["id"])

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Vector store built with {len(documents)} protocols.")