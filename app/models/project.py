from .base_model import BaseModel

class Project(BaseModel, table=True):
    __tablename__ = "project"

    name: str
    description: str
