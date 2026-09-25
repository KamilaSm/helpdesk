from datetime import datetime
from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str


class CommentOut(BaseModel):
    id: int
    text: str
    ticket_id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}