import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field

# Define a database model
class BaseModel(SQLModel):
    """
    Base model for all database models.
    id: UUID = The primary key of the model.
    created_at: datetime = The timestamp of when the model was created.
    updated_at: datetime = The timestamp of when the model was last updated.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
