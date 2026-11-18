from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse

from engine.core import AIEngine
from engine.models import NSFWModel
from api.validators import validate_image

app = FastAPI(
    title="AI Guard API",
    description="AI-powered NSFW image detection API",
    version="0.1.0"
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal server error"
            }
        }
    )

model = NSFWModel("Falconsai/nsfw_image_detection")
engine = AIEngine(model, threshold=0.7)


@app.get("/")
def home():
    return {
        "message": "AI Guard API is running",
        "status": "online"
    }


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    image = validate_image(file)

    result = engine.analyze(image)

    return {
        "success": True,
        "data": {
            "filename": file.filename,
            "label": result.label,
            "score": result.score,
            "model": result.model_name,
            "threshold": result.threshold
        }
    }
