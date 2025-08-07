from datetime import datetime
from typing import Optional
from sqlalchemy import Column, BigInteger
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel, table = True):
    # Base model with BigInteger ID to match your PostgreSQL schema
    __abstract__ = True
    
    id: Optional[int] = Field(
        default = None, 
        primary_key = True,
        sa_column = Column(BigInteger, primary_key = True)
    )


class SoftDeleteMixin(SQLModel):
    # Soft delete pattern used throughout your database
    is_deleted: bool = Field(default = False)


class LookupTableBase(BaseModel, SoftDeleteMixin, table = True):
    # Base for lookup tables (order_types, priority_types, etc.)
    __abstract__ = True
    
    code: str = Field(max_length = 50, unique = True)
    name: str = Field(max_length = 100)
    sort_order: int = Field(default = 0)


class SortableTableBase(BaseModel, SoftDeleteMixin, table = True):
    # Base for tables with sort_order and auto-assignment triggers
    __abstract__ = True
    
    sort_order: int = Field(default = 0)


class DivisionBaseModel(BaseModel, SoftDeleteMixin, table = True):
    # Base for division-related tables
    __abstract__ = True
    
    code: str = Field(max_length = 50)
    name: str = Field(max_length = 100)
    parent_id: Optional[int] = Field(default = None, foreign_key = "divisions.id")
    sort_order: int = Field(default = 0)


class OrderBaseModel(BaseModel, SoftDeleteMixin, table = True):
    # Base for order-related entities
    __abstract__ = True
    
    type_id: int = Field(foreign_key = "order_types.id")
    status_id: int = Field(foreign_key = "order_statuses.id")
    priority_id: Optional[int] = Field(default = None, foreign_key = "priority_types.id")
    initiator_id: int = Field(foreign_key = "divisions.id")
    create_date: datetime = Field(default_factory = lambda: datetime.now(datetime.timezone.utc))


class AssignmentBaseModel(BaseModel, SoftDeleteMixin, table = True):
    # Base for assignment-related entities
    __abstract__ = True
    
    order_id: int = Field(foreign_key = "orders.id")
    status_id: int = Field(foreign_key = "assignment_statuses.id")
    priority_id: Optional[int] = Field(default = None, foreign_key = "priority_types.id")
    executor_id: int = Field(foreign_key = "users.id")
    target_type_id: int = Field(foreign_key = "target_types.id")
    assignment_type_id: int = Field(foreign_key = "assignment_types.id")


class TransferBaseModel(BaseModel, SoftDeleteMixin, table = True):
    # Base for transfer-related entities
    __abstract__ = True
    
    assignment_id: int = Field(foreign_key = "assignments.id")
    from_recipient_id: int = Field(foreign_key = "divisions.id")
    to_recipient_id: int = Field(foreign_key = "divisions.id")
    transfer_type_id: int = Field(foreign_key = "transfer_types.id")
    status_id: int = Field(foreign_key = "transfer_statuses.id")
    category_id: Optional[int] = Field(default = None, foreign_key = "transfer_categories.id")
    effective_date: datetime = Field(default_factory = lambda: datetime.now(datetime.timezone.utc))
    due_date: Optional[datetime] = Field(default = None)
    completion_date: Optional[datetime] = Field(default = None)
    is_active: bool = Field(default = False)
    order_id: Optional[int] = Field(default = None, foreign_key = "orders.id")


class TransferItemBaseModel(BaseModel, SoftDeleteMixin, table = True):
    # Base for transfer items
    __abstract__ = True
    
    transfer_id: int = Field(foreign_key = "transfers.id")
    item_type_id: int = Field(foreign_key = "item_types.id")
    item_identifier: Optional[str] = Field(default = None, max_length = 100)
    quantity: float = Field(gt = 0)
    unit_of_measure: str = Field(max_length = 50)
    description: Optional[str] = Field(default = None)
    is_active: bool = Field(default = False)


class UserBaseModel(BaseModel, SoftDeleteMixin, table = True):
    # Base for user-related entities
    __abstract__ = True
    
    username: str = Field(max_length = 100, unique = True)
    is_active: bool = Field(default = True)
    is_admin: bool = Field(default = False)


class AuditLogBaseModel(BaseModel, table = True):
    # Base for audit logging (no soft delete for audit records)
    __abstract__ = True
    
    table_name: str = Field(max_length = 100)
    record_id: int = Field()
    action: str = Field(max_length = 50)
    user_id: Optional[int] = Field(default = None, foreign_key = "users.id")
    action_timestamp: datetime = Field(default_factory = lambda: datetime.now(datetime.timezone.utc))
    details: Optional[str] = Field(default = None)
    is_deleted: bool = Field(default = False)


# API Schema base classes for Pydantic models
class BaseResponse(SQLModel):
    # Base response schema
    id: int