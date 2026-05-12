from pydantic import BaseModel
from http_routes.dto.route_data_trip_status_request_dto import RouteDataTripStatusRequestDTO

class RouteDataTripHistoryRequestDTO(BaseModel):
    expectedInstitutionsPassed: list[str]
    actualInstitutionsPassed: list[str]
    status: list[RouteDataTripStatusRequestDTO]