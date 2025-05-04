import re
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.db import engine
from app.helper import logger, verify_token
from app.models import User, UserRole, Permission, PermissionType,RolePermission

def rolebase_middleware(full_request: Request, request: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    This middleware is used to check user is able to access or not
    """

    # extract token
    token = request.credentials
    logger.info({
        "message": "(rolebase_middleware) middleware is running",
        "token": token
    })

    # verify token
    decoded_token = verify_token(token)
    logger.debug({
        "message": "(rolebase_middleware) decoded token",
        "decoded_token": decoded_token
    })

    if not decoded_token:
        logger.error({
            "message": "(rolebase_middleware) Invalid token",
            "token": token
        })

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Is Expired"
        )
    
    if decoded_token["type"] != "access":
        logger.error({
            "message": "(rolebase_middleware) Invalid token type",
            "token": token
        })

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token Type"
        )
    
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.id == decoded_token["user_id"])
        ).first()

        # close session
        session.close()

    logger.debug({
        "message": "(rolebase_middleware) user",
        "user": user
    })

    if not user:
        logger.error({
            "message": "(rolebase_middleware) User not found",
            "user_id": decoded_token["user_id"]
        })

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    
    # fetch user role permission
    with Session(engine) as session:
        user_role = session.exec(
            select(UserRole).where(UserRole.user_id == user.id)
        ).first()

        # close session
        session.close()
    logger.debug({
        "message": "(rolebase_middleware) user role",
        "user_role": user_role
    })

    # fetch permission detail
    with Session(engine) as session:
        user_role = session.exec(
            select(UserRole).where(UserRole.user_id == user.id)
        ).first()

        if not user_role:
            logger.error({
                "message": "(rolebase_middleware) User role not found",
                "user_id": user.id
            })

            # close session
            session.close()

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Role Not Found"
            )
        
        permissions = session.exec(
            select(Permission).join(RolePermission, Permission.id == RolePermission.permission_id).where(RolePermission.role_id == user_role.role_id)
        ).all()

        # close session
        session.close()

    logger.debug({
        "message": "(rolebase_middleware) permissions",
        "permissions": permissions,
        "path": full_request.url.path,
        "method": full_request.method
    })

    # check user is able to access or not
    is_allowed = False
    for permission in permissions:
        is_path_allowed = re.match(rf"{permission.permission_routes}", full_request.url.path)
        logger.debug({
            "message": "(rolebase_middleware) is path allowed",
            "is_path_allowed": is_path_allowed,
        })

        if is_path_allowed and (full_request.method.lower() == permission.permission_type.value or permission.permission_type == PermissionType.ADMIN):
            is_allowed = True
            break
    
    logger.debug({
        "message": "(rolebase_middleware) is allowed",
        "is_allowed": is_allowed
    })

    if is_allowed == False:
        raise HTTPException(status_code=401, detail="Not Have Enough Permission")
    
    return user
