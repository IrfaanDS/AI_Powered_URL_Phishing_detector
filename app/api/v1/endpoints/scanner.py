from fastapi import APIRouter, HTTPException
from app.schemas.url_schema import URLRequest, ScanResponse
from app.services.extractor import extract_all_signals
from app.services.classifier import classify_with_gemini

router = APIRouter()

@router.post("/scan", response_model=ScanResponse)
async def scan_url(request: URLRequest):
    try:
        # 1. Run the extraction pipeline
        signals = extract_all_signals(str(request.url))
        
        # 2. Get AI Decision
        report = classify_with_gemini(signals)
        
        return {
            "url": request.url,
            "decision": report.get('decision', 'UNKNOWN'),
            "confidence": report.get('confidence', 'LOW'),
            "details": report.get('reasoning', 'No reasoning provided')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
