from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger
from app.models import Project

def list_project_handler(limit: int = 10, offset: int = 0):
    """
    List Project handler
    """
    logger.info({
        "message": "(list_project_handler)Getting Project",
        "limit": limit,
        "offset": offset,
    })

    try:
        # get projects
        with Session(engine) as session:
            projects = session.exec(
                select(Project).offset(offset).limit(limit)
            ).all()

            # close session
            session.close()

        logger.debug({
            "message": "(list_project_handler)Project found",
            "project": projects,
        })

        # return project
        return {
            "projects": projects,
        }

    except Exception as e:
        logger.error({
            "message": "(list_project_handler)Error getting project",
            "error": str(e),
        })

        # raise exception if error getting project
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting projects",
        )
