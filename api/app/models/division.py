from typing import Optional
from sqlmodel import Field
from .base import DivisionBaseModel


class Division(DivisionBaseModel, table=True):
    __tablename__ = "divisions"
    
    # Additional fields from your database schema
    short_name: Optional[str] = Field(default=None, max_length=100)
    is_internal: bool = Field(default=False)
