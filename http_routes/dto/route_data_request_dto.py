from datetime import time
from pydantic import BaseModel

from http_routes.dto.route_data_trip_history_request_dto import RouteDataTripHistoryRequestDTO

class RouteContentRequestDTO(BaseModel):
    expected_going: time
    expected_going_finish: time
    expected_return: time
    expected_return_finish: time

    shift: str
    recurring_days: list[str]
    trip_history: list[RouteDataTripHistoryRequestDTO]