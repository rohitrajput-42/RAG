from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["rag_db"]
collection = db["documents"]

def fetch_all_documents():
    documents = collection.find({}, {"_id": 0})
    return list(documents)