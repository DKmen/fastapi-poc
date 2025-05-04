from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger
from app.models import User

def get_user_handler(user_id: UUID):
    """
    Get user handler
    """
    logger.info({
        "message": "(get_user_handler)Getting user",
        "user_id": user_id,
    })

    try:
        # get user
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.id == user_id)
            ).first()

            # close session
            session.close()
        
        logger.debug({
            "message": "(get_user_handler)User retrieved",
            "user_id": user_id,
            "user": user,
        })

        if not user:
            logger.error({
                "message": "(get_user_handler)User Not Found",
                "user_id": user_id,
            })

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found",
            )

        return {
            "message": "User Retrieved",
            "user": user,
        }
    
    except HTTPException as e:
        logger.error({
            "message": "(get_user_handler)Error getting user",
            "user_id": user_id,
            "error": e,
        })
        
        raise e
    
    except Exception as e:
        logger.error({
            "message": "(get_user_handler)Error getting user",
            "user_id": user_id,
            "error": e,
        })

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error Getting User",
        )
