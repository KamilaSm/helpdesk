from fastapi import FastAPI
from app.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router

app = FastAPI(title=settings.APP_NAME)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
@app.get("/health")
def health_check():
    return {"status": "ok"}
