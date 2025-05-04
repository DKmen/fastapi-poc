from uuid import UUID
from fastapi import APIRouter, Depends

from app.middleware import rolebase_middleware

from .functions import get_user_handler, list_user_handler, create_user_handler, CreateUserPayload

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/", dependencies=[
    Depends(rolebase_middleware)
])
def get_user(user_id: UUID):
    """
    Description:
    - Get user by id
    - It only access by admin
    """
    return get_user_handler(user_id)

@router.get("/list", dependencies=[
    Depends(rolebase_middleware)
])
def list_users(limit: int = 10, offset: int = 0):
    """
    Description:
    - List users
    - It only access by admin
    """
    return list_user_handler(offset, limit)

@router.post("/", dependencies=[
    Depends(rolebase_middleware)
])
def create_user(payload: CreateUserPayload):
    """
    Description:
    - Create user
    - It only access by admin
    """
    return create_user_handler(payload)
