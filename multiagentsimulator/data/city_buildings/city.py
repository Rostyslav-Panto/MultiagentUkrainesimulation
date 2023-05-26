import osmnx as ox
from folium import folium

from shapely.geometry import Point

class City:
    def __init__(
            self,
            lat=None,
            lng=None,
            distance=None,
    ):
        self.lat = 50.4501 if lat is None else lat
        self.lng = 30.5234 if lng is None else lng
        self.distance = 2000 if distance is None else distance

    def get_classified_buildings_in_distance(self):
        all_buildings = ox.geometries_from_point(
            (self.lat, self.lng),
            tags={'building': True},
            dist=self.distance
        )
        all_buildings = all_buildings[~all_buildings['geometry'].apply(lambda geom: isinstance(geom, Point))]
        classified_building = {
            "University": all_buildings[
                all_buildings['building'].isin(['university', 'college', 'collage'])
            ],
            "Office": all_buildings[
                all_buildings['building'].isin(['office'])
            ],
            "Restaurant": all_buildings[
                all_buildings['building'].isin(['commercial'])
            ],
            "School": all_buildings[
                all_buildings['building'].isin(['school'])
            ],
            "Hospital": all_buildings[all_buildings['building'].isin(['hospital', 'clinic'])],
            "Store": all_buildings[all_buildings['building'].isin(['supermarket','shop','mall'])],
            "Home":all_buildings[all_buildings['building'].isin([
                'house',
                'apartments',
                'semidetached_house',
                'allotment_house',
                'warehouse',
            ])],
        }

        return classified_building

    def get_map(self, zoom=15):
        return folium.Map(location=[self.lat, self.lng], zoom_start=zoom)

