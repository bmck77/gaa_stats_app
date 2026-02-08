## Dockerfile for the FastAPI backend
## Builds an image that runs the FastAPI app using Uvicorn.
FROM python:3.11-slim
WORKDIR /app
# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy source
COPY . .
# Expose default FastAPI port
EXPOSE 8000
# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
