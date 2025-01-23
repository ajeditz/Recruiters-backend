import requests
import json

# API endpoint
url = "http://localhost:9000/candidates"

# Function to batch upload candidates
def batch_upload(candidates):
    success_count = 0
    for candidate in candidates:
        try:
            response = requests.post(url, json=candidate)
            if response.status_code == 201:
                success_count += 1
                print(f"Uploaded: {candidate['name']}")
            else:
                print(f"Failed to upload: {candidate['name']} - Status Code: {response.status_code}")
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error uploading {candidate['name']}: {e}")
    
    print(f"\nBatch upload completed: {success_count}/{len(candidates)} uploaded successfully.")



if __name__ == "__main__":
    # Path to JSON file containing candidate profiles
    json_file_path = "candidates.json"
    with open(json_file_path,'r') as file:
        candidates=json.load(file)
    # Load and upload candidate profiles
    # Execute the batch upload
    batch_upload(candidates)
