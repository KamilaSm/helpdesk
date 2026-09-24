from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str = "medium"


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    org_id: int
    created_by: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}