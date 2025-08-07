from typing import Optional
from sqlmodel import SQLModel, Field


class DivisionCreate(SQLModel):
    # Input schema for creating divisions
    code: str = Field(max_length=50)
    name: str = Field(max_length=100)
    short_name: Optional[str] = Field(default=None, max_length=100)
    parent_id: Optional[int] = None
    sort_order: Optional[int] = 0
    is_internal: bool = False


class DivisionUpdate(SQLModel):
    # Input schema for updating divisions - all fields optional
    code: Optional[str] = Field(default=None, max_length=50)
    name: Optional[str] = Field(default=None, max_length=100)
    short_name: Optional[str] = Field(default=None, max_length=100)
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_internal: Optional[bool] = None
    is_deleted: Optional[bool] = None
