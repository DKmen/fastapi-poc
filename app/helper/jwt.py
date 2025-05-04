import jwt
import datetime

from app.constants import config
from .logger import logger

def generate_token(payload: dict, exp_min = 30):
    """
    Generate token using payload and secret key
    Args:
        payload (dict): payload to be encoded
        exp_min (int, optional): expiration time in minutes. Defaults to 30.
    Returns:
        str: token
    """
    # start logging
    logger.info({
        "message": "(generate_token)Generate token started",
        "payload": payload,
        "exp_min": exp_min,
    })

    if(exp_min != -1):
        # set expiration time
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_min)

        # add expiration time to payload
        payload.update({"exp": exp})

    logger.info({
        "message": "(generate_token)Payload updated",
        "payload": payload,
    })

    # generate token using secret key
    return jwt.encode(payload, config["SECRET_TOKEN"], algorithm="HS256")

def verify_token(token: str):
    """
    Verify token using secret key
    Args:
        token (str): token to be verified
    Returns:
        bool: True if token is valid, False otherwise
    """
    logger.info({
        "message": "(verify_token)Verify token started",
        "token": token,
    })

    try:
        # verify token using secret key
        payload = jwt.decode(token, config["SECRET_TOKEN"], algorithms=["HS256"])
        logger.info({
            "message": "(verify_token)Token verified",
            "payload": payload,
        })

        # return payload
        return payload
    except jwt.ExpiredSignatureError as e:
        logger.error({
            "message": "(verify_token)Token expired",
            "error": e,
        })

        return False
    except jwt.InvalidTokenError as e:
        logger.error({
            "message": "(verify_token)Invalid token",
            "error": e,
        })

        return False
