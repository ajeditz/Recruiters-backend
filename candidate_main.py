from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, firestore, initialize_app
import os

from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# Initialize Firebase
CRED_PATH=os.getenv("CRED_PATH")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred)
db = firestore.client()

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


