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
    """
    contains the list of the different users to generate the certificate for
    """
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
    
    


class CertificateRequestModel(BaseModel):
    """
    The model for the pixel fly bulk certification generation

    ```
    {
  templateId: string;
  template: {
    imageUrl: string;
    width: number;
    height: number;
    fields: Array<{
      id: string;
      type: "text" | "date" | "image";
      x: number;
      y: number;
      width: number;
      height: number;
      value: string;
    }>;
  };
  data: Array<{
    name: string;
    date?: string;
    image?: string;
    [key: string]: string | undefined;
  }>;
}
    ```
    """
    template_id: str = Field(..., min_length=3)
    template_data:TemplateData
    data: Data

    