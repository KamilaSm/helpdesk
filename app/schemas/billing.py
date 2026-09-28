from typing import Optional
from pydantic import BaseModel


class UsageOut(BaseModel):
    plan: str
    used: int
    limit: Optional[int]  # None = без лимита


class PlanChange(BaseModel):
    plan_id: int