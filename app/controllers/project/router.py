from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends

from app.middleware import rolebase_middleware

from .functions import get_project_handler, list_project_handler, delete_project_handler, create_project_handler, update_project_handler, CreateProjectPayload, UpdateProjectPayload

router = APIRouter(prefix="/project", tags=["Project"])

@router.get("/", dependencies=[
    Depends(rolebase_middleware)
])
def get_project(project_id: UUID):
    """
    Description:
    - Get project by id
    - User and Admin can access this endpoint
    """
    return get_project_handler(project_id)

@router.get("/list", dependencies=[
    Depends(rolebase_middleware)
])
def list_project(offset: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Description:
    - List all projects
    - User and Admin can access this endpoint
    """
    return list_project_handler(limit, offset)

@router.delete("/", dependencies=[
    Depends(rolebase_middleware)
])
def delete_project(project_id: UUID):
    """
    Description:
    - Delete project by id
    - Admin can access this endpoint
    """
    return delete_project_handler(project_id)

@router.post("/", dependencies=[
    Depends(rolebase_middleware)
])
def create_project(payload: CreateProjectPayload):
    """
    Description:
    - Create project
    - Admin can access this endpoint
    """
    return create_project_handler(payload)

@router.patch("/", dependencies=[
    Depends(rolebase_middleware)
])
def update_project(project_id:UUID, payload: UpdateProjectPayload):
    """
    Description:
    - Update project
    - Admin can access this endpoint
    """
    return update_project_handler(project_id, payload)
