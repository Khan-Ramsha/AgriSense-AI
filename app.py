from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
import os
from src.components.model_config import ModelConfig
from src.components.plant_image_analyzer import PlantImageAnalyzer

load_dotenv()

app = FastAPI(
    title="Plant Analysis API",
    description="API for analyzing plant images using WatsonX AI."
)

# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

model_config = ModelConfig(
    model_id="meta-llama/llama-3-2-90b-vision-instruct",
    api_key=os.getenv("APIKEY"),
    project_id=os.getenv("PROJECT_ID"),
    url="https://au-syd.ml.cloud.ibm.com"
)

plant_analyzer = PlantImageAnalyzer(model_config)


@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(..., description="Upload the plant image to analyze"),
    query: str = Form(..., description="Provide the query for the plant image")
):
    try:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        image_contents = await image.read()
        encoded_image = plant_analyzer.encode_image(image_contents)
        
        response = plant_analyzer.analyze_plant_image(query, encoded_image)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
