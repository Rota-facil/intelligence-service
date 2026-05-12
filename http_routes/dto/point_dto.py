from pydantic import BaseModel

class PointDto(BaseModel):
    latitude: float
    longitude: float