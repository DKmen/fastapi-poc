from enum import Enum

from sqlmodel import Field
from .base_model import BaseModel

class PermissionType(Enum):
    ADMIN = "admin"
    POST = "post"
    GET = "get"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"

class Permission(BaseModel, table=True):
    __tablename__ = "permission"

    name: str
    permission_routes : str
    permission_type : PermissionType = Field(default=PermissionType.GET,nullable=False)
