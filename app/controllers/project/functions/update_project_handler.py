from typing import Optional
from pydantic import BaseModel
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger
from app.models import Project

class UpdateProjectPayload(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

def update_project_handler(project_id: UUID, payload: UpdateProjectPayload):
    """
    Update project handler
    """
    logger.info({
        "message": "(update_project_handler)Updating project",
        "payload": payload,
    })

    try:
        with Session(engine) as session:
            # get project
            project = session.exec(
                select(Project).where(Project.id == project_id)
            ).first()

            if payload.name is not None:
                project.name = payload.name
            if payload.description is not None:
                project.description = payload.description

            # add project to session
            session.add(project)
            # commit session
            session.commit()
            # refresh project
            session.refresh(project)

            # close session
            session.close()
        
        logger.debug({
            "message": "(update_project_handler)Project updated",
            "project": project,
        })

        return {
            "message": "Project updated",
            "project": project,
        }
        
    except Exception as e:
        logger.error({
            "message": "(update_project_handler)Error updating project",
            "error": str(e),
        })

        # raise exception if error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error Updating Project",
        )

