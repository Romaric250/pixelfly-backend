from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class NewFlyerRequest(BaseModel):
    name: str
    template_type: str  
    images: List[HttpUrl]
    created_at: Optional[datetime] = None
