from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import date

load_dotenv()

app = FastAPI()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client["journal"]
entries = db["entries"]

class Entry(BaseModel):
    title: str
    content: str
    date: date
    tags: list[str] = []

@app.get("/")
def read_root():
    return {"message": "Journal API is running"}

@app.post("/entries")
async def create_entry(entry: Entry):
    doc = entry.dict()
    doc["date"] = doc["date"].isoformat()
    result = entries.insert_one(doc)
    return {"message": "Entry created", "id": str(result.inserted_id)}

@app.get("/entries")
def get_entries():
    entries_list = []
    for entry in entries.find().sort("date", -1):
        entry["_id"] = str(entry["_id"])
        entries_list.append(entry)
    return entries_list

@app.delete("/entries/{entry_id}")
async def delete_entry(entry_id: str):
    result = entries.delete_one({"_id": ObjectId(entry_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry deleted"}

@app.put("/entries/{entry_id}")
async def update_entry(entry_id: str, entry: Entry):
    doc = entry.dict()
    doc["date"] = doc["date"].isoformat()  # Convert date to string
    result = entries.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": doc}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry updated"}