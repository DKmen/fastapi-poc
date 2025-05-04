from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, delete

from app.db import engine
from app.helper import logger
from app.models import Project

def delete_project_handler(project_id: UUID):
    """
    Delete project handler
    """
    logger.info({
        "message": "(delete_project_handler)Deleting project",
        "project_id": project_id,
    })

    try:
        # delete project
        with Session(engine) as session:
            session.exec(
                delete(Project).where(Project.id == project_id)
            )

            # commit changes
            session.commit()

            # close session
            session.close()
        
        logger.info({
            "message": "(delete_project_handler)Project deleted",
            "project_id": project_id,
        })

        return {
            "message": "Project Deleted Successfully"
        }
    
    except Exception as e:
        logger.error({
            "message": "(delete_project_handler)Error deleting project",
            "project_id": project_id,
            "error": str(e),
        })
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error Deleting Project",
        )
