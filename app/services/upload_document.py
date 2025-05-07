import os
import uuid
from fastapi import FastAPI, HTTPException, UploadFile, File
from pymongo import MongoClient
import openai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["rag_db"]
collection = db["documents"]

model = SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text, chunk_size=200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def get_embeddings(chunks):
    return model.encode(chunks).tolist()

def index_embeddings(embeddings, metadata):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, "index.faiss")

async def save_document(file: UploadFile):
    content = (await file.read()).decode("utf-8")
    chunks = split_text(content)
    embeddings = get_embeddings(chunks)

    document = {
        "_id": str(uuid.uuid4()),
        "filename": file.filename,
        "content": content,
        "embedding": embeddings
    }

    result = collection.insert_one(document)
    index_embeddings(embeddings, {"document_id": str(result.inserted_id)})

    return {"document_id": str(result.inserted_id)}