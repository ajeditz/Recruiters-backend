from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional,List
from firebase_admin import credentials, firestore, initialize_app
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Firebase
CRED_PATH=os.getenv("CRED_PATH")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred)
db = firestore.client()

# FastAPI app
app = FastAPI()

# Firestore collection name for recruiters
RECRUITERS_COLLECTION = "recruiters"

from datetime import datetime

class Recruiter(BaseModel):
    profile_picture_url: str
    recruiter_name: str
    recruiter_rating: float
    location: str
    verified_badge: bool
    num_candidates_listed: int
    tags: list[str]
    bio: str
    successful_deals: int
    created_at: datetime | None = None  # Auto-managed
    updated_at: datetime | None = None  # Auto-managed


@app.post("/recruiters/", status_code=201)
async def create_recruiter(recruiter: Recruiter):
    try:
        timestamp = datetime.utcnow()
        recruiter_data = recruiter.model_dump()
        recruiter_data["created_at"] = timestamp
        recruiter_data["updated_at"] = timestamp

        # Add recruiter to Firestore
        new_recruiter_ref = db.collection(RECRUITERS_COLLECTION).document()
        new_recruiter_ref.set(recruiter_data)
        return {"id": new_recruiter_ref.id, "message": "Recruiter profile created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recruiters/{recruiter_id}")
async def read_recruiter(recruiter_id: str):
    try:
        recruiter_ref = db.collection(RECRUITERS_COLLECTION).document(recruiter_id)
        recruiter = recruiter_ref.get()
        if not recruiter.exists:
            raise HTTPException(status_code=404, detail="Recruiter not found")
        return recruiter.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/recruiters/{recruiter_id}")
async def update_recruiter(recruiter_id: str, recruiter: Recruiter):
    try:
        recruiter_ref = db.collection(RECRUITERS_COLLECTION).document(recruiter_id)
        if not recruiter_ref.get().exists:
            raise HTTPException(status_code=404, detail="Recruiter not found")
        
        recruiter_data = recruiter.dict(exclude_unset=True)
        recruiter_data["updated_at"] = datetime.utcnow()
        recruiter_ref.update(recruiter_data)
        return {"message": "Recruiter profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/recruiters/{recruiter_id}")
async def delete_recruiter(recruiter_id: str):
    try:
        recruiter_ref = db.collection(RECRUITERS_COLLECTION).document(recruiter_id)
        if not recruiter_ref.get().exists:
            raise HTTPException(status_code=404, detail="Recruiter not found")
        recruiter_ref.delete()
        return {"message": "Recruiter profile deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/recruiters/search")
async def search_recruiters(tags: List[str] ):
    """
    Search recruiters by tags.
    """
    recruiters = db.collection(RECRUITERS_COLLECTION).stream()
    recruiter_list = [recruiter.to_dict() for recruiter in recruiters]
    

    matching_recruiters = [
        recruiter for recruiter in recruiter_list
        if any(tag.lower() in [t.lower() for t in recruiter["tags"]] for tag in tags)
    ]
    
    if not matching_recruiters:
        raise HTTPException(status_code=404, detail="No recruiters found matching the given tags.")
    
    return {"results": matching_recruiters}

@app.get("/recruiters/")
async def list_recruiters():
    try:
        recruiters = db.collection(RECRUITERS_COLLECTION).stream()
        recruiter_list = [recruiter.to_dict() for recruiter in recruiters]
        return recruiter_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

