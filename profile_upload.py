import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from firebase_admin import credentials, firestore, initialize_app
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Initialize Firebase
cred = credentials.Certificate(os.getenv('CRED_PATH'))
initialize_app(cred)
db = firestore.client()

app = FastAPI()


@app.post("/upload-profile-picture")
async def upload_profile_picture( file: UploadFile = File(...)):
    try:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(file.file)
        image_url = upload_result.get('secure_url')

        if not image_url:
            raise HTTPException(status_code=400, detail="Failed to upload image to Cloudinary.")

        # Update Firestore with the image URL
        # user_ref = db.collection('users').document(user_id)
        # user_ref.update({'profile_pic_url': image_url})

        return JSONResponse(status_code=200, content={"message": "Profile picture uploaded successfully.", "image_url": image_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
