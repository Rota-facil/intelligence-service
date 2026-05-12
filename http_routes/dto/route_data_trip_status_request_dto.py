from datetime import datetime

from pydantic import BaseModel

class RouteDataTripStatusRequestDTO(BaseModel):
    progress: str
    delay: str
    eventOccurred: datetime