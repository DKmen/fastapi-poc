from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger, verify_token, generate_token
from app.models import User

def refresh_handler(token:str):
    logger.debug({
        "message": "(refresh_handler)Token",
        "token": token,
    })

    try:
        # decrypt token
        decoded_token = verify_token(token)
        logger.debug({
            "message": "(refresh_handler)Decoded token",
            "decoded_token": decoded_token,
        })

        if not decoded_token:
            logger.error({
                "message": "(refresh_handler)Invalid token",
                "token": token,
            })
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh Token Is Expired",
            )
        
        with Session(engine) as session:
            # fetch user from database
            user = session.exec(
                select(User).where(User.id == decoded_token["user_id"])
            ).first()
        
            # close session
            session.close()
        
        # check if user exists or not
        if not user:
            logger.error({
                "message": "(refresh_handler)User not found",
                "token": token,
            })

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found",
            )
        
        # generate access token
        access_token = generate_token({
            "user_id": str(user.id),
            "email": user.email,
            "role": decoded_token["role"],
            "type": "access"
        },60)

        return {
            "access_token": access_token,
            "user":{
                "id": str(user.id),
                "email": user.email,
                "role": decoded_token["role"],
            }
        }
    
    except HTTPException as e:
        logger.error({
            "message": "(refresh_handler)HTTPException",
            "error": e,
        })
        
        raise e
    
    except Exception as e:
        logger.error({
            "message": "(refresh_handler)Exception",
            "error": e,
        })

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
