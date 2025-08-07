from typing import List, Optional
from sqlmodel import Session, select, and_, or_

from app.models.division import Division
from app.schemas.division import DivisionCreate, DivisionUpdate


# Business exceptions
class DivisionNotFoundError(Exception):
    def __init__(self, division_id: int):
        self.division_id = division_id
        super().__init__(f"Division with ID {division_id} not found")


class DivisionCodeExistsError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Division with code '{code}' already exists")


class ParentNotFoundError(Exception):
    def __init__(self, parent_id: int):
        self.parent_id = parent_id
        super().__init__(f"Parent division with ID {parent_id} not found")


class CircularReferenceError(Exception):
    def __init__(self):
        super().__init__("Cannot create circular parent-child relationship")


class SelfParentError(Exception):
    def __init__(self):
        super().__init__("Division cannot be its own parent")


class HasChildrenError(Exception):
    def __init__(self, children_count: int = 0):
        self.children_count = children_count
        super().__init__(f"Cannot delete division with {children_count} child divisions")


class DivisionNotDeletedError(Exception):
    def __init__(self, division_id: int):
        self.division_id = division_id
        super().__init__(f"Division with ID {division_id} is not deleted")


class DivisionService:
    # Business logic for division operations
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 20,
        include_deleted: bool = False,
        search: Optional[str] = None,
        active_only: bool = True
    ) -> List[Division]:
        # Get divisions with filtering and pagination
        query = select(Division)
        
        # Apply filters
        filters = []
        if not include_deleted:
            filters.append(Division.is_deleted == False)
        if active_only:
            filters.append(Division.is_active == True)
        
        if filters:
            query = query.where(and_(*filters))
        
        # Search functionality
        if search:
            search_filter = or_(
                Division.code.ilike(f"%{search}%"),
                Division.name.ilike(f"%{search}%"),
                Division.short_name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        # Apply pagination and ordering
        query = query.order_by(Division.sort_order, Division.name)
        query = query.offset(skip).limit(limit)
        
        return self.db.exec(query).all()
    
    def get_list(
        self, 
        include_deleted: bool = False,
        search: Optional[str] = None,
        active_only: bool = True
    ) -> List[Division]:
        # Get all divisions without pagination
        query = select(Division)
        
        # Apply filters
        filters = []
        if not include_deleted:
            filters.append(Division.is_deleted == False)
        if active_only:
            filters.append(Division.is_active == True)
        
        if filters:
            query = query.where(and_(*filters))
        
        # Search functionality
        if search:
            search_filter = or_(
                Division.code.ilike(f"%{search}%"),
                Division.name.ilike(f"%{search}%"),
                Division.short_name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        # Apply ordering
        query = query.order_by(Division.sort_order, Division.name)
        
        return self.db.exec(query).all()
    
    def get_by_id(self, division_id: int, include_deleted: bool = False) -> Optional[Division]:
        # Get division by ID
        query = select(Division).where(Division.id == division_id)
        
        if not include_deleted:
            query = query.where(Division.is_deleted == False)
        
        return self.db.exec(query).first()
    
    def get_by_code(self, code: str, include_deleted: bool = False) -> Optional[Division]:
        # Get division by code (unique identifier)
        query = select(Division).where(Division.code == code)
        
        if not include_deleted:
            query = query.where(Division.is_deleted == False)
        
        return self.db.exec(query).first()
    
    def create(self, division_data: DivisionCreate) -> Division:
        # Create new division with business logic validation
        
        # Check if code already exists
        existing = self.get_by_code(division_data.code, include_deleted=True)
        if existing:
            raise DivisionCodeExistsError(division_data.code)
        
        # Validate parent exists if provided
        if division_data.parent_id:
            parent = self.get_by_id(division_data.parent_id)
            if not parent:
                raise ParentNotFoundError(division_data.parent_id)
        
        # Auto-assign sort_order if not provided
        if division_data.sort_order is None or division_data.sort_order == 0:
            division_data.sort_order = self._get_next_sort_order(division_data.parent_id)
        
        # Create division
        division = Division.model_validate(division_data)
        self.db.add(division)
        self.db.commit()
        self.db.refresh(division)
        
        return division
    
    def update(self, division_id: int, update_data: DivisionUpdate) -> Optional[Division]:
        # Update division with business logic validation
        division = self.get_by_id(division_id)
        if not division:
            raise DivisionNotFoundError(division_id)
        
        # Check code uniqueness if being updated
        if update_data.code and update_data.code != division.code:
            existing = self.get_by_code(update_data.code, include_deleted=True)
            if existing:
                raise DivisionCodeExistsError(update_data.code)
        
        # Validate parent exists if being updated
        if update_data.parent_id is not None:
            if update_data.parent_id == division_id:
                raise SelfParentError()
            
            if update_data.parent_id != 0:  # 0 means root level
                parent = self.get_by_id(update_data.parent_id)
                if not parent:
                    raise ParentNotFoundError(update_data.parent_id)
                
                # Check for circular references
                if self._would_create_cycle(division_id, update_data.parent_id):
                    raise CircularReferenceError()
        
        # Apply updates
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(division, field, value)
        
        self.db.commit()
        self.db.refresh(division)
        
        return division
    
    def delete(self, division_id: int, soft_delete: bool = True) -> bool:
        # Delete division (soft or hard)
        division = self.get_by_id(division_id)
        if not division:
            raise DivisionNotFoundError(division_id)
        
        # Check if division has children
        children = self.get_children(division_id)
        if children:
            raise HasChildrenError(len(children))
        
        if soft_delete:
            division.is_deleted = True
            self.db.commit()
        else:
            self.db.delete(division)
            self.db.commit()
        
        return True
    
    def get_children(self, parent_id: int, include_deleted: bool = False) -> List[Division]:
        # Get child divisions
        query = select(Division).where(Division.parent_id == parent_id)
        
        if not include_deleted:
            query = query.where(Division.is_deleted == False)
        
        query = query.order_by(Division.sort_order, Division.name)
        
        return self.db.exec(query).all()
    
    def get_hierarchy_tree(self, root_id: Optional[int] = None) -> List[Division]:
        # Get full hierarchy tree using recursive query
        # This would use PostgreSQL CTE for complex hierarchies
        if root_id:
            return self._get_subtree(root_id)
        else:
            # Get all root level divisions and their children
            roots = self.db.exec(
                select(Division)
                .where(Division.parent_id.is_(None))
                .where(Division.is_deleted == False)
                .order_by(Division.sort_order)
            ).all()
            return roots
    
    def move_division(self, division_id: int, new_parent_id: Optional[int], new_sort_order: Optional[int] = None) -> Division:
        # Move division to new parent with sort order management
        division = self.get_by_id(division_id)
        if not division:
            raise DivisionNotFoundError(division_id)
        
        # Validate new parent
        if new_parent_id:
            if new_parent_id == division_id:
                raise SelfParentError()
            
            if self._would_create_cycle(division_id, new_parent_id):
                raise CircularReferenceError()
        
        # Update parent and sort order
        old_parent_id = division.parent_id
        division.parent_id = new_parent_id
        
        if new_sort_order is not None:
            division.sort_order = new_sort_order
        else:
            division.sort_order = self._get_next_sort_order(new_parent_id)
        
        self.db.commit()
        self.db.refresh(division)
        
        # Reorder siblings in old parent
        if old_parent_id != new_parent_id:
            self._reorder_siblings(old_parent_id)
        
        return division
    
    def get_available_codes(self, prefix: Optional[str] = None) -> List[str]:
        # Get list of available division codes with optional prefix filter
        all_divisions = self.get_list(active_only = True)
        codes = [div.code for div in all_divisions]
        
        if prefix:
            codes = [code for code in codes if code.startswith(prefix.upper())]
        
        return sorted(codes)
    
    def restore(self, division_id: int) -> Division:
        # Restore a soft-deleted division
        division = self.get_by_id(division_id, include_deleted = True)
        if not division:
            raise DivisionNotFoundError(division_id)
            
        if not division.is_deleted:
            raise DivisionNotDeletedError(division_id)
        
        # Restore by updating is_deleted to False
        restore_data = DivisionUpdate(is_deleted = False)
        return self.update(division_id, restore_data)
    
    # Private helper methods
    def _get_next_sort_order(self, parent_id: Optional[int]) -> int:
        # Get next available sort order for siblings
        query = select(Division.sort_order).where(Division.parent_id == parent_id)
        if parent_id is None:
            query = query.where(Division.parent_id.is_(None))
        
        max_order = self.db.exec(query.order_by(Division.sort_order.desc())).first()
        return (max_order or 0) + 10
    
    def _would_create_cycle(self, division_id: int, potential_parent_id: int) -> bool:
        # Check if setting potential_parent_id as parent would create a cycle
        current_id = potential_parent_id
        while current_id:
            if current_id == division_id:
                return True
            parent = self.get_by_id(current_id)
            current_id = parent.parent_id if parent else None
        return False
    
    def _get_subtree(self, root_id: int) -> List[Division]:
        # Get division and all its descendants
        # This could use recursive CTE for deep hierarchies
        division = self.get_by_id(root_id)
        if not division:
            return []
        
        result = [division]
        children = self.get_children(root_id)
        for child in children:
            result.extend(self._get_subtree(child.id))
        
        return result
    
    def _reorder_siblings(self, parent_id: Optional[int]) -> None:
        # Reorder siblings after deletion/move
        siblings = self.get_children(parent_id)
        for i, sibling in enumerate(siblings):
            sibling.sort_order = (i + 1) * 10
        self.db.commit()


# Service factory function
def get_division_service(db: Session) -> DivisionService:
    return DivisionService(db)
