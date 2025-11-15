from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class CreateRequest(BaseModel):
    category: str
    region: Optional[str] = None
    short_text: Optional[str] = None
    phone: Optional[str] = None
    consent: bool = False

class RequestOut(CreateRequest):
    id: str
    status: str
    created_at: datetime
    assigned_to: Optional[str] = None

class PartnerIn(BaseModel):
    name: str
    region: str
    contact: str
    type: str
    notes: Optional[str] = None

class WebhookPayload(BaseModel):
    type: str
    user_id: str
    text: Optional[str] = None
    button_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

