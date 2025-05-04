from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.helper import logger, decrypt_string, generate_token
from app.db import engine
from app.models import User, UserRole

class LoginHandlerPayload(BaseModel):
    email: str
    password: str

def login_handler(payload: LoginHandlerPayload):
    logger.debug({
        "message": "(login_handler)Login handler started",
        "payload": payload,
    })

    try:
        with Session(engine) as session:
            # fetch user from database
            user = session.exec(
                select(User).where(User.email == payload.email)
            ).first()

            # close session
            session.close()

        # check if user exists or not
        if not user:
            logger.error({
                "message": "(login_handler)User not found",
                "payload": payload,
            })

            # raise exception if user not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found",
            )
        
        # check if password is correct
        user_password = decrypt_string(user.password)
        logger.debug({
            "message": "(login_handler)User password",
            "password": payload.password,
            "user_password": user_password,
        })

        if payload.password != user_password:
            logger.error({
                "message": "(login_handler)Password is incorrect",
                "payload": payload,
            })

            # raise exception if password is incorrect
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is incorrect",
            )

        # fetch user role
        with Session(engine) as session:
            # fetch user role
            user_role = session.exec(
                select(UserRole).where(UserRole.user_id == user.id)
            ).first()

            # close session
            session.close()
        logger.debug({
            "message": "(login_handler)User role",
            "user_role": user_role,
        })

        # generate access token
        access_token = generate_token({
            "user_id": str(user.id),
            "email": user.email,
            "role": str(user_role.role_id),
            "type": "access"
        },60)

        # generate refresh token
        refresh_token = generate_token({
            "user_id": str(user.id),
            "email": user.email,
            "role": str(user_role.role_id),
            "typr": "refresh"
        },60*24*7)

        logger.info({
            "message": "(login_handler)Login handler success",
            "payload": payload,
            "access_token": access_token,
            "refresh_token": refresh_token,
        })

        # return access token
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user":{
                "id": str(user.id),
                "email": user.email,
                "role": str(user_role.role_id),
            }
        }

    except HTTPException as e:
        logger.error({
            "message": "(login_handler)User not found",
            "payload": payload,
            "error": str(e),
        })

        raise e

    except Exception as e:
        logger.error({
            "message": "(login_handler)Login handler failed",
            "payload": payload,
            "error": str(e),
        })

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login handler failed",
        )
