import firebase_admin
from firebase_admin import credentials, firestore
from fastapi.middleware.cors import CORSMiddleware

cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth

async def get_current_user(request: Request):
    id_token = request.headers.get('Authorization')
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

from fastapi import FastAPI, Depends

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
async def check_profile(uid: str = Depends(get_current_user)):
    user_ref = db.collection('users').document(uid)
    user_doc = user_ref.get()
    if user_doc.exists:
        return {"profile_exists": True}
    else:
        return {"profile_exists": False}
