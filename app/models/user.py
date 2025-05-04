from sqlmodel import UniqueConstraint
from .base_model import BaseModel

class User(BaseModel, table=True):
    __tablename__ = "user"

    name: str
    email: str
    password: str

    __table_args__ = (
        UniqueConstraint("email", name="uk_user_email"),
    )

