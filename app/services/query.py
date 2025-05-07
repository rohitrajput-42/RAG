from pymongo import MongoClient
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["rag_db"]
collection = db["documents"]

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("index.faiss")


llm_client = OpenAI(
    api_key="", #Add API key here#
    base_url="https://api.groq.com/openai/v1",
)

def retrieve_context(query: str, k: int = 3) -> str:
    query_embedding = embedding_model.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), k)

    docs = []
    for idx in I[0]:
        if idx == -1:
            continue
        doc = collection.find_one({"embedding_index": idx})
        if doc:
            docs.append(doc["content"])

    return "\n".join(docs)

def get_llm_response(query: str) -> str:
    context = retrieve_context(query)

    messages = [
        {"role": "system", "content": "Answer based on the context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    try:
        response = llm_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
