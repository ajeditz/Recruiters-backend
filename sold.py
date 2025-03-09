import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import random
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Firebase
CRED_PATH=os.getenv("CRED_PATH")
cred = credentials.Certificate(CRED_PATH)
initialize_app(cred)
db = firestore.client()

# Reference to the collection where candidates are stored
CANDIDATES_COLLECTION = "candidates"

# Fetch all candidate documents
candidates_ref = db.collection(CANDIDATES_COLLECTION).stream()

# Loop through all candidate records and update with "sold" field
for candidate in candidates_ref:
    candidate_id = candidate.id  # Get the document ID
    random_sold_value = random.randint(0, 10)  # Generate random number

    # Update Firestore document
    db.collection(CANDIDATES_COLLECTION).document(candidate_id).update({"sold": random_sold_value})
    print(f"Updated candidate {candidate_id} with sold = {random_sold_value}")

print("Successfully updated all candidate profiles!")
