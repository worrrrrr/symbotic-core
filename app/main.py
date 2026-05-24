from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.hybrid_intent_parser import HybridSymbolicThaiParser

app = FastAPI(
    title="SYMBOTIC CORE v1.8",
    description="Symbolic Hybrid Thai NLP Intent Engine",
    version="1.8"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

parser = HybridSymbolicThaiParser()

class QueryRequest(BaseModel):
    text: str

@app.post("/process")
async def process_query(request: QueryRequest):
    result = parser.parse(request.text)
    
    if not result:
        return {
            "status": "error",
            "message": "ไม่สามารถเข้าใจคำสั่งได้ (Confidence ต่ำ)",
            "confidence": 0
        }
    
    return {
        "status": "success",
        "intent": result["intent"],
        "confidence": result["confidence"],
        "slots": result["slots"],
        "preprocessed_text": result.get("preprocessed_text")
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.8", "system": "Symbotic Core"}
