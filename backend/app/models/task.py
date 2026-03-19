from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID
class TaskCreate(BaseModel):
    meeting_id = UUID
    task = str
    owner = str
    due_date = date

class TaskResponse(BaseModel):
    id = str
    meeting_id = UUID
    task = str
    owner = Optional[str]
    due_date = Optional[date]
    created_at = datetime
    status = bool

    