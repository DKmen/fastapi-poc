from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger, encrypt_string
from app.models import User
from app.models.role import Role
from app.models.user_role import UserRole

class CreateUserPayload(BaseModel):
    name: str
    email: str
    password: str

def create_user_handler(payload: CreateUserPayload):
    """
    Create user handler
    """
    logger.info({
        "message": "(create_user_handler)Creating user",
        "payload": payload,
    })

    try:
        # create user
        with Session(engine) as session:
            user = User(
                name=payload.name,
                email=payload.email,
                password=encrypt_string(payload.password),
            )

            # add user to database
            session.add(user)
            # commit changes
            session.commit()

            # refresh user
            session.refresh(user)

            # close session
            session.close()

        # attech user role
        with Session(engine) as session:
            # fetch user role id
            role = session.exec(
                select(Role).where(Role.name == "User")
            ).first()

            # add user role to user
            user_role = UserRole(
                user_id=user.id,
                role_id=role.id,
            )

            # add user role to session
            session.add(user_role)
            # commit changes
            session.commit()
            # refresh user role
            session.refresh(user_role)

            # close session
            session.close()
        
        logger.debug({
            "message": "(create_user_handler)User created",
            "payload": payload,
            "user": user,
            "user_role": user_role,
        })

        del user.password

        return {
            "message": "User Ceated",
            "user": user,
        }

    except Exception as e:
        logger.error({
            "message": "(create_user_handler)Error creating user",
            "payload": payload,
            "error": str(e),
        })

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )