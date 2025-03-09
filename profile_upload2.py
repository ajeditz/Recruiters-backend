import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.getenv("CRED_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()

from pydantic import BaseModel

class UserProfileRequest(BaseModel):
    user_id: str


from fastapi import FastAPI, HTTPException, Query
from google.cloud.firestore_v1.document import DocumentSnapshot

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with a list of origins to restrict.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods. Adjust as needed.
    allow_headers=["*"],  # Allows all headers. Adjust as needed.
)


@app.get("/check-profile")
async def check_profile(user_id: str = Query(..., description="The ID of the user to check")):
    """
    Check if a user profile exists in the Firestore database.

    Args:
        user_id (str): The ID of the user to check.

    Returns:
        dict: A dictionary indicating whether the profile exists.
    """
    try:
        user_ref = db.collection('recruiters').document(user_id)
        doc = user_ref.get()
        if doc.exists:
            return {"profile_exists": True}
        else:
            return {"profile_exists": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
