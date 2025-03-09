from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import uuid
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Firebase
CRED_PATH=os.getenv("CRED_PATH")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with a list of origins to restrict.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods. Adjust as needed.
    allow_headers=["*"],  # Allows all headers. Adjust as needed.
)


CANDIDATE_COLLECTION="candidate_required"


# Candidate Post Schema
class CandidatePost(BaseModel):
    name: str
    location: str
    notice_period: int
    recruiter_id: str
    role: str
    skills: List[str]
    contact_no: str
    email: EmailStr
    expected_ctc: str
    experience: float
    linkedin_profile_url: Optional[str]
    fulfilled: Optional[bool] = False  # Defaults to False
    created_at: datetime | None = None  # Auto-managed
    updated_at: datetime | None = None  # Auto-managed
    

# **1. API to Create a Candidate Required Post**
@app.post("/post-candidate/")
async def post_candidate(data: CandidatePost):
    post_id = str(uuid.uuid4())  # Generate a unique ID for each post
    data_dict = data.model_dump()
    data_dict["post_id"] = post_id

    try:
        db.collection("candidate_posts").document(post_id).set(data_dict)
        return {"message": "Post created successfully", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# **2. API to Fetch All Candidate Required Posts**
@app.get("/get-candidate-posts/")
async def get_candidate_posts():
    try:
        posts = db.collection("candidate_posts").stream()
        post_list = [post.to_dict() for post in posts]
        return {"posts": post_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# **3. API to Mark a Post as Fulfilled**
@app.put("/fulfill-post/{post_id}")
async def fulfill_post(post_id: str):
    post_ref = db.collection("candidate_posts").document(post_id)
    post = post_ref.get()

    if not post.exists:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        post_ref.update({"fulfilled": True})
        return {"message": "Post marked as fulfilled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
