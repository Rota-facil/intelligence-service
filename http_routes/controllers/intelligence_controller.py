from fastapi import APIRouter
from http_routes.dto.point_request_dto import PointRequestDto
from http_routes.dto.route_data_request_dto import RouteContentRequestDTO
from business.heat_maps_service import HeatMapService
from business.open_ai_service import OpenAIService
router = APIRouter(prefix="/intelligence")


heat_map_service = HeatMapService()
open_ai_service = OpenAIService()

@router.get("/")
async def heath_check():
    return "intelligence-service is running"

@router.get("/route/heat-map")
async def generate_heat_map(locations: list[PointRequestDto]):
    heat_map_service.make_heat_map(locations)
    return 'testando'

@router.post("/route/interpretation")
async def generate_route_interpretation(route_content: RouteContentRequestDTO):
    route_interpretation = open_ai_service.generate_route_interpretation(route_content)
    return {
        'routeInterpretation': route_interpretation
    }
