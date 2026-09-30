from fastapi import FastAPI
from app.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.tickets import router as tickets_router
from app.api.comments import router as comments_router
from app.api.billing import router as billing_router
from contextlib import asynccontextmanager
from app.scheduler import start_scheduler, scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(tickets_router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(comments_router, prefix="/api/v1/tickets", tags=["comments"])
app.include_router(billing_router, prefix="/api/v1/billing", tags=["billing"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
