from datetime import time
from pydantic import BaseModel

from http_routes.dto.route_data_trip_history_request_dto import RouteDataTripHistoryRequestDTO

class RouteContentRequestDTO(BaseModel):
    expectedGoing: time
    expectedGoingFinish: time
    expectedReturn: time
    expectedReturnFinish: time

    shift: str
    recurringDays: list[str]
    tripHistory: list[RouteDataTripHistoryRequestDTO]