from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger
from app.models import User

def list_user_handler(offset: int = 0, limit: int = 10):
    """
    List user handler
    """
    logger.info({
        "message": "(list_user_handler)Listing users",
        "offset": offset,
        "limit": limit,
    })

    try:
        # list users
        with Session(engine) as session:
            users = session.exec(
                select(User).offset(offset).limit(limit)
            ).all()
            
            # close session
            session.close()
        
        logger.debug({
            "message": "(list_user_handler)Users listed",
            "offset": offset,
            "limit": limit,
            "users": users,
        })

        return {
            "message": "Users Listed",
            "users": users,
        }
    
    except Exception as e:
        logger.error({
            "message": "(list_user_handler)Error listing users",
            "offset": offset,
            "limit": limit,
            "error": str(e),
        })

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error listing users",
        )
