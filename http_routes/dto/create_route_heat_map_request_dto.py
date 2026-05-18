import uuid

from http_routes.dto.point_request_dto import PointRequestDto
from http_routes.dto.current_user import CurrentUser
from pydantic import BaseModel
from  uuid import UUID

class RouteHeatMapRequestDTO(BaseModel):
    currentUser: CurrentUser
    routeId: UUID
    points: list[PointRequestDto]