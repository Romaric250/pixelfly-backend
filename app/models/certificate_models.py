from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional


class CertificateRequest(BaseModel):
    name: constr(min_length=1)
    course_name: constr(min_length=1)
    created_at: Optional[datetime] = None
