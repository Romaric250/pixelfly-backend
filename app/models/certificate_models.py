from pydantic import BaseModel, constr, Field
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class CertificateRequest(BaseModel):
    name: constr(min_length=1)
    course_name: constr(min_length=1)
    created_at: Optional[datetime] = None

class FieldDataType(str, Enum):
    """
    Enum for the type of field the user has chosen in the frontend
    """
    text = "text"
    date = "date"
    image = "image"

class FieldData(BaseModel):
    """
    contains all the fields for the individual data the user has selected on the frontend
    """
    id: str = Field(..., min_length=1)
    type: FieldDataType
    x: int = Field(..., min_length=1)
    y: int = Field(..., min_length=1)
    width: int = Field(..., min_length=1)
    height: int = Field(..., min_length=1)
    value: str = Field(..., min_length=1)

class Data(BaseModel):
    name : str = Field(..., min_length=5)
    date : str = Field(...)
    image : str = Field(...)
    key: Dict[str, str] = Field(...) 


class TemplateData(BaseModel):
    """
    Template data here
    """
    imageurl: str = Field(..., min_length=1)
    width: int = Field(...,min_length=1)
    height: int = Field(...,min_length=1)
    fields : FieldData
    data: Data 
    
    


class CertRequestModel(BaseModel):
    template_id: str = Field(..., min_length=3)
    template_data:TemplateData


    