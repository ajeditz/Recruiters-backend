# Use official Python image as base
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy only the required files first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "profile_upload2:app", "--host", "0.0.0.0", "--port", "8000"]
