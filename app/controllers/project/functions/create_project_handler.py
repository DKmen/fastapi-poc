from pydantic import BaseModel
from sqlmodel import Session

from app.db import engine
from app.helper import logger
from app.models import Project

class CreateProjectPayload(BaseModel):
    name: str
    description: str

def create_project_handler(payload: CreateProjectPayload):
    """
    Create project handler
    """
    logger.info({
        "message": "(create_project_handler)Creating project",
        "payload": payload,
    })

    with Session(engine) as session:
        # create project
        project = Project(
            name=payload.name,
            description=payload.description,
        )

        # add project to session
        session.add(project)
        # commit session
        session.commit()

        # refresh project
        session.refresh(project)

        # close session
        session.close()

    logger.info({
        "message": "(create_project_handler)Project created",
        "project": project,
    })

    return {
        "message": "Project Created",
        "data": project,
    }
