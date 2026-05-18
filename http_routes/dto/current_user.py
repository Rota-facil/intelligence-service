from pydantic import BaseModel
from uuid import UUID

class CurrentUser(BaseModel):
    userId: UUID
    prefectureId: UUID
    email: str
    role: str