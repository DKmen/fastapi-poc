from .base_model import BaseModel

class Role(BaseModel, table=True):
    __tablename__ = "role"

    name: str
