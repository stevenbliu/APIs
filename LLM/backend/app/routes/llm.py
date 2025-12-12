from fastapi import APIRouter
from app.models import ModelRequest
from app.llm import request_gemini

router = APIRouter(prefix="/gemini", tags=["items"])


@router.post("/generate")
def generate(model_request: ModelRequest):
    prompt = model_request.prompt
    temperature = model_request.temperature
    max_tokens = model_request.max_tokens

    response = request_gemini(prompt, temperature, max_tokens)
    

    return response
