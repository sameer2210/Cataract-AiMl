from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import shutil
import uuid
import os
import logging

from app.predictor import predict_image

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cataract-service")

# FastAPI application
app = FastAPI(
    title="Cataract Detection API",
    description="Production-grade AI inference service for cataract classification.",
    version="1.0.0",
)

# Use /tmp for Cloud Run read-only root filesystem compatibility
TEMP_DIR = os.environ.get("TEMP_DIR", "/tmp/cataract_temp")
os.makedirs(TEMP_DIR, mode=0o700, exist_ok=True)

# Security constraints: Max 10 MB upload size limit and allowed MIME types
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/jpg", "image/webp"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler to prevent internal stack trace disclosure (OWASP API3:2023).
    """
    logger.error(f"Unhandled error processing request {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred while processing the request."}
    )


@app.get("/")
def home():
    return {
        "message": "Cataract AI Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "cataract-detection",
        "model_loaded": True
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    # 1. Validate MIME type
    content_type = file.content_type or ""
    if content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{content_type}'. Allowed types: {', '.join(sorted(ALLOWED_MIME_TYPES))}"
        )

    # 2. Generate secure random filename to prevent Path Traversal (OWASP API1:2023)
    safe_filename = f"{uuid.uuid4().hex}.png"
    temp_path = os.path.join(TEMP_DIR, safe_filename)

    # Prevent path traversal escape validation
    if not os.path.abspath(temp_path).startswith(os.path.abspath(TEMP_DIR)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file path trajectory detected."
        )

    file_size = 0
    try:
        # 3. Stream buffer with size enforcement to prevent Memory/Disk DoS (OWASP API4:2023)
        with open(temp_path, "wb") as buffer:
            while chunk := await file.read(64 * 1024):  # 64 KB chunking
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE_BYTES:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES // (1024*1024)} MB."
                    )
                buffer.write(chunk)

        # 4. Perform EfficientNet-B3 prediction
        prediction, confidence = predict_image(temp_path)

        return {
            "prediction": prediction,
            "confidence": float(confidence)
        }

    finally:
        # 5. Guaranteed cleanup block to prevent disk space leaks on success or exception
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as cleanup_err:
                logger.warning(f"Failed to cleanup temp file {temp_path}: {cleanup_err}")