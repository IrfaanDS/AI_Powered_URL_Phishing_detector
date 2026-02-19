from pydantic import BaseModel, HttpUrl
from typing import Optional

class URLRequest(BaseModel):
    url: HttpUrl

class ScanResponse(BaseModel):
    url: HttpUrl
    decision: str
    confidence: str
    details: str
