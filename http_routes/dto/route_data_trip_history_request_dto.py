from pydantic import BaseModel
from http_routes.dto.route_data_trip_status_request_dto import RouteDataTripStatusRequestDTO

class RouteDataTripHistoryRequestDTO(BaseModel):
    expected_institutions_passed: list[str]
    actual_institutions_passed: list[str]
    status: list[RouteDataTripStatusRequestDTO]