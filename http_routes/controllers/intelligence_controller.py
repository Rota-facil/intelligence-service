from fastapi import APIRouter
from http_routes.dto.point_dto import PointDto
from business.heat_maps_service import HeatMapService
router = APIRouter(prefix="/intelligence")


heat_map_service = HeatMapService()

@router.get("/")
async def generate_heat_map(locations: list[PointDto]):
    heat_map_service.make_heat_map(locations)
    return 'testando'