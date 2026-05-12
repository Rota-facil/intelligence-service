from pydantic import BaseModel

class PointRequestDto(BaseModel):
    latitude: float
    longitude: float