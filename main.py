from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.api_v1 import router as api_v1_router

app = FastAPI(
    title="Guruji Astrology API Engine",
    description="Backend REST API Service for Guruji Astrology App - Kundli, Daily Rashifal, Panchang, Numerology & AI Astrologer Chat",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Flutter Client App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_v1_router)

@app.get("/")
def root():
    return {
        "app": "Guruji Astrology Backend Service",
        "status": "online",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
