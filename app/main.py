from fastapi import FastAPI
from app.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.tickets import router as tickets_router
from app.api.comments import router as comments_router


app = FastAPI(title=settings.APP_NAME)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(tickets_router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(comments_router, prefix="/api/v1/tickets", tags=["comments"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
