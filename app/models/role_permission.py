from uuid import UUID
from sqlmodel import Field, UniqueConstraint
from .base_model import BaseModel

class RolePermission(BaseModel, table=True):
    __tablename__ = "role_permission"

    permission_id : UUID = Field(foreign_key="permission.id",nullable=False)
    role_id : UUID = Field(foreign_key="role.id",nullable=False)

    __table_args__ = (
        UniqueConstraint("permission_id", "role_id", name="uk_role_permission_permission_id_role_id"),
    )
