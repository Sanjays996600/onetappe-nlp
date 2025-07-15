from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Import our intent handler
from nlp.intent_handler import parse_command, detect_language
from nlp.enhanced_multilingual_parser import parse_multilingual_command, format_response

# Define request and response models
class CommandRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class CommandResponse(BaseModel):
    intent: str
    entities: Dict[str, Any]
    language: str
    confidence: float = 1.0  # Default to 1.0 for rule-based matching
    raw_text: str
    normalized_text: str

class CommandInput(BaseModel):
    text: str

# Create FastAPI app
app = FastAPI(
    title="OneTappe WhatsApp Backend",
    version="1.0.0",
    description="Handles WhatsApp-based commerce actions"
)

router = APIRouter()

@router.post("/api/parse-command", response_model=CommandResponse)
async def handle_command(request: CommandRequest):
    """
    Parse a WhatsApp command and return the recognized intent and entities
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Detect language
    language = detect_language(request.message)
    
    # Parse the command
    result = parse_command(request.message)
    
    # Return structured response
    return CommandResponse(
        intent=result["intent"],
        entities=result["entities"],
        language=result.get("language", language),
        raw_text=result.get("raw_text", request.message),
        normalized_text=result.get("normalized_text", request.message.lower().strip())
    )

@router.get("/api/supported-intents")
async def get_supported_intents():
    """
    Return a list of supported intents and example commands
    """
    return {
        "intents": {
            "get_inventory": ["Show my products", "List all products"],
            "get_low_stock": ["Show low stock items", "List products with low stock"],
            "get_report": ["Send today's report", "Get this week's report"],
            "add_product": ["Add new product Rice 50rs 20qty", "Create product Sugar 25 15"],
            "edit_stock": ["Edit stock of Rice to 100", "Update Wheat stock to 75"],
            "get_orders": ["Show my orders", "List recent orders"]
        },
        "languages": ["en", "hi"]
    }

@router.post("/process", summary="Parse WhatsApp command", tags=["NLP Parser"])
def process_command(data: CommandInput):
    result = parse_multilingual_command(data.text)
    response = format_response(
        intent=result.get("intent"),
        entities=result.get("entities", {}),
        language=result.get("language"),
        raw_text=result.get("raw_text"),
        normalized_text=result.get("normalized_text")
    )
    return response

# Include router in the app
app.include_router(router)

# Example of how to run the API server
if __name__ == "__main__":
    import uvicorn
    print("Starting WhatsApp Command Intent Handler API...")
    print("Visit http://localhost:8000/docs for API documentation")
    uvicorn.run(app, host="0.0.0.0", port=8000)