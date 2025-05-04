from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger
from app.models import Project

def get_project_handler(project_id: UUID):
    """
    Get Project handler
    """
    logger.info({
        "message": "(get_project_handler)Getting project",
        "project_id": project_id,
    })

    try:
        # get project
        with Session(engine) as session:
            project = session.exec(
                select(Project).where(Project.id == project_id)
            ).first()

            # close session
            session.close()

        # check if project exists or not
        if not project:
            logger.error({
                "message": "(get_project_handler)Project not found",
                "project_id": project_id,
            })

            # raise exception if project not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project Not Found",
            )
        
        logger.info({
            "message": "(get_project_handler)Project found",
            "project": project,
        })

        # return project
        return {
            "project": project,
        }
    
    except HTTPException as e:
        logger.error({
            "message": "(get_project_handler)Project not found",
            "project_id": project_id,
            "error": str(e),
        })

        # raise exception if project not found
        raise e

    except Exception as e:
        logger.error({
            "message": "(get_project_handler)Error getting project",
            "project_id": project_id,
            "error": str(e),
        })

        # raise exception if error getting project
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting project",
        )
