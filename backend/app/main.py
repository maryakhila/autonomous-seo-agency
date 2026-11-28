
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.clients import router as clients_router

app = FastAPI(
    title="AI SEO Agency API",
    description="Private AI-powered SEO agency platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    clients_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "AI SEO Agency API is running"
    }


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI SEO Agency API"
    }
