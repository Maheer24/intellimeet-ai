from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# Create Class - contains fields that will be provided by either user or llms, no auto generated db fields
# Response Class - Output to client, for frontend

class MeetingCreate(BaseModel):
    title = Optional[str]
    transcript = str
    summary = str

class MeetingResponse(BaseModel):
    title = Optional[str]
    summary = str
    meeting_id = UUID
    created_at: datetime