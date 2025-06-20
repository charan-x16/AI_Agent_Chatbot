from fastapi import APIRouter
from fastapi.responses import JSONResponse
from APP.models import RequestState
from agents.AI_Agent import get_response_from_ai_agent


router = APIRouter()

ALLOWED_MODEL_NAMES = ["llama3-70b-8192", "gemini-2.5-flash"]

@router.post("/chat")
def chat_endpoint(request: RequestState):
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    response = get_response_from_ai_agent(
        llm_id=request.model_name,
        provider=request.model_provider,
        query=request.messages,
        system_prompt=request.system_prompt,
        allow_search=request.allow_search,
    )
    return JSONResponse(response)