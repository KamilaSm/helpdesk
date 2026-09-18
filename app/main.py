from fastapi import FastAPI
from app.config import settings
from app.api.auth import router as auth_router

app = FastAPI(title=settings.APP_NAME)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
