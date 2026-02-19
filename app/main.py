from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI(title="Phishing Detector API", version="1.0")

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Phishing Detector API is running"}
