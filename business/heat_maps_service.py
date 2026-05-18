import pandas as pd
import plotly.express as px
import requests

from http_routes.dto.create_route_heat_map_request_dto import RouteHeatMapRequestDTO
from http_routes.dto.point_request_dto import PointRequestDto


import os

BASE_FILE_SERVICE_URL = os.environ.get("BASE_FILE_SERVICE_URL", "http://localhost:8088")


class HeatMapService:
    def make_heat_map(self, route_heat_map: RouteHeatMapRequestDTO):
        data_frame = self.__build_data_frame(route_heat_map.points)
        fig = self.__build_density_map(data_frame)

        img_bytes = fig.to_image(format="png")

        files = {
            "file": (
                "heatmap.png",
                img_bytes,
                "image/png"
            )
        }

        current_user = route_heat_map.currentUser

        response = requests.post(
            f"{BASE_FILE_SERVICE_URL} + /heat-map/ + {route_heat_map.routeId}",
            files=files,
            headers= {
                'x-user-id': current_user.userId,
                'x-user-email': current_user.email,
                'x-user-role': current_user.role,
                'x-prefecture-id': current_user.prefectureId,
            }
        )

        response.raise_for_status()

        file_response = response.json()

        presigned_url = file_response["presignedUrl"]

        return presigned_url

    def __build_data_frame(self, locations: list[PointRequestDto]):
        latitude = []
        longitude = []

        for location in locations:
            latitude.append(location.latitude)
            longitude.append(location.longitude)

        df = pd.DataFrame({
            "lat": latitude,
            "lon": longitude
        })

        return df

    def __build_density_map(self, df: pd.DataFrame):
        return px.density_map(
            df,
            lat="lat",
            lon="lon",
            radius=10,
            zoom=15,
            map_style="open-street-map"
        )