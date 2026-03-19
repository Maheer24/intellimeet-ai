from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class EmailCreate(BaseModel):
    meeting_id = UUID
    recipient = str
    email_body = str 

class EmailResponse(BaseModel):
    id = str
    meeting_id = UUID
    recipient = str
    email_body = str 
    sent = Optional[bool]
    created_at = datetime
