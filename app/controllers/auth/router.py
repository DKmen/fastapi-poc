from fastapi import APIRouter

from .functions import login_handler , refresh_handler, LoginHandlerPayload

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(payload: LoginHandlerPayload):
    """
    Description:
    - This function is used to login user
    - This function will return access token and refresh token if success
    - This function will return user id, email, and role
    """
    return login_handler(payload)

@router.post("/refresh")
def refresh_token(token: str):
    """
    Description:
    - This function is used to refresh token
    - This function will return access token if success
    - This function will return user id, email, and role
    """
    return refresh_handler(token)
