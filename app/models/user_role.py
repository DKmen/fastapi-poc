from uuid import UUID
from sqlmodel import Field, UniqueConstraint
from .base_model import BaseModel

class UserRole(BaseModel, table=True):
    __tablename__ = "user_role"

    user_id : UUID = Field(foreign_key="user.id",nullable=False)
    role_id : UUID = Field(foreign_key="role.id",nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uk_user_id_role_id"),
    )
