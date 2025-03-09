from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional,List
import uuid
from firebase_admin import credentials, firestore, initialize_app
import os
from fastapi.middleware.cors import CORSMiddleware
import difflib
from dotenv import load_dotenv

load_dotenv()
# Initialize Firebase
CRED_PATH=os.getenv("CRED_PATH")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred)
db = firestore.client()

# FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with a list of origins to restrict.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods. Adjust as needed.
    allow_headers=["*"],  # Allows all headers. Adjust as needed.
)

# Firestore collection name for recruiters
RECRUITERS_COLLECTION = "recruiters"

from datetime import datetime

class Recruiter(BaseModel):
    recruiter_id: str = None  # Added recruiter_id field
    profile_picture_url: str
    recruiter_name: str
    recruiter_rating: int
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
        recruiter_id=str(uuid.uuid4())
        recruiter.recruiter_id=recruiter_id
        timestamp = datetime.utcnow()
        recruiter_data = recruiter.model_dump()
        recruiter_data["created_at"] = timestamp
        recruiter_data["updated_at"] = timestamp

        # Add recruiter to Firestore
        new_recruiter_ref = db.collection(RECRUITERS_COLLECTION).document(document_id=recruiter_id)
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
    


@app.post("/recruiters/search")
async def search_recruiters(tags: List[str], threshold: float = 0.6):
    """
    Search recruiters by tags using fuzzy matching.
    """
    recruiters = db.collection(RECRUITERS_COLLECTION).stream()
    recruiter_list = [recruiter.to_dict() for recruiter in recruiters]
    
    matching_recruiters = []
    
    for recruiter in recruiter_list:
        recruiter_tags = [tag.lower() for tag in recruiter.get("tags", [])]
        for tag in tags:
            matches = difflib.get_close_matches(tag.lower(), recruiter_tags, cutoff=threshold)
            if matches:
                matching_recruiters.append(recruiter)
                break
    
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



CANDIATE_COLLECTION='candidates'

class Candidate(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the candidate")
    recruiter_id: str
    name: str
    experience: int  # in years
    role: str
    contact_number: str
    email: EmailStr
    linkedin_profile_url: str
    skills: List[str]
    location: str  # city, country
    notice_period: str  # e.g., "30 days", "Immediate"
    expected_ctc: str  # e.g., "50k/month", "$60/hour"
    sold:int = Field(0,description="How many times the candidate profile has been sold")


# Create a candidate
@app.post("/candidates/", status_code=201)
async def create_candidate(candidate: Candidate):
    candidate_data = candidate.model_dump()
    candidate_ref = db.collection("candidates").document()
    candidate_data["id"] = candidate_ref.id
    candidate_ref.set(candidate_data)
    return candidate_data

# Get all candidates for a recruiter
@app.get("/candidates/{recruiter_id}", response_model=List[Candidate])
async def get_candidates_for_recruiter(recruiter_id: str):
    candidates_ref = db.collection("candidates").where("recruiter_id", "==", recruiter_id).stream()
    candidates = [candidate.to_dict() for candidate in candidates_ref]
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidates found for this recruiter.")
    return candidates

# Get a specific candidate
@app.get("/candidate/{id}", response_model=Candidate)
async def get_candidate(id: str):
    candidate_ref = db.collection("candidates").document(id).get()
    if not candidate_ref.exists:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    return candidate_ref.to_dict()

# Update a candidate
@app.put("/candidate/{id}", response_model=Candidate)
async def update_candidate(id: str, updated_data: Candidate):
    candidate_ref = db.collection("candidates").document(id)
    candidate = candidate_ref.get()
    if not candidate.exists:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    candidate_ref.update(updated_data.dict(exclude_unset=True))
    updated_candidate = candidate_ref.get().to_dict()
    return updated_candidate

# Delete a candidate
@app.delete("/candidate/{id}", status_code=204)
async def delete_candidate(id: str):
    candidate_ref = db.collection("candidates").document(id)
    if not candidate_ref.get().exists:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    candidate_ref.delete()
    return {"message": "Candidate deleted successfully."}



