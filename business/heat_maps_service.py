import pandas as pd
import plotly.express as px
from http_routes.dto.point_request_dto import PointRequestDto


class HeatMapService:
    def make_heat_map(self, locations: list[PointRequestDto]):
        data_frame = self.__build_data_frame(locations)
        fig = self.__build_density_map(data_frame)
        fig.write_image("heatmap.png")

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