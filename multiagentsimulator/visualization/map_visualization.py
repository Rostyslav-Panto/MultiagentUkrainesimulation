import random
from typing import Sequence

import folium
import geopandas
from folium import GeoJson, CircleMarker, FeatureGroup
from folium.plugins import TimestampedGeoJson
from shapely.geometry import Point

from multiagentsimulator.data.city_buildings.city import City
from multiagentsimulator.environment import SimulationState, Location, Home, Store, University, School, \
    Hospital, Restaurant, Office, InfectionSummary


def generate_random_points(number, polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points


class MapViz:
    _city: City

    def __init__(
            self,
            locations: Sequence[Location],
            city: City,
    ):
        self._map = city.get_map()
        self._states_on_stage = {}
        self._locations = locations
        self._city = city

    def record_state(self, state: SimulationState) -> None:
        stage_dict = {}
        for person, person_state in state.id_to_person_state.items():
            stage_dict.setdefault(person_state.current_location.name, []).append(
                (person,
                person_state.infection_state)
            )
        self._states_on_stage[str(state.sim_time)] = (stage_dict)

    def plot(self) -> None:
        locations_colors = {
            Hospital: 'red',
            Store: 'blue',
            School: 'green',
            Restaurant: 'purple',
            University: 'orange',
            Office: 'darkred',
            Home: "grey",
        }
        persons_colors = {
            InfectionSummary.CRITICAL: 'red',
            InfectionSummary.RECOVERED: 'blue',
            InfectionSummary.NONE: 'green',
            InfectionSummary.INFECTED: 'yellow',
            InfectionSummary.DEAD: "grey",
        }
        buildings = FeatureGroup(name='buildings', control=False)
        for sim_time, stage in self._states_on_stage.items():
            persons_layer = FeatureGroup(name=f'{sim_time}')

            for location in self._locations:
                sim_geo = geopandas.GeoSeries(location.position)
                geo_j = sim_geo.to_json()
                geo_j = GeoJson(
                    name=str(type(location)),
                    data=geo_j,
                    style_function=lambda feature, name=type(location): {'fillColor': locations_colors[name],
                                                                         'color': locations_colors[name],
                                                                         'fillOpacity': 0.5,
                                                                         },
                )
                geo_j.add_to(buildings)

                persons = stage.get(location.id.name)
                if persons is not None:
                    points = generate_random_points(
                        polygon=location.position,
                        number=len(persons)
                    )
                    for point, person in zip(points, persons):
                        CircleMarker(
                            location=(point.y, point.x),
                            radius=2,
                            color=persons_colors[person[1].summary],
                            fillColor=persons_colors[person[1].summary],
                            fill=True,
                        ).add_to(persons_layer)
                print(location.id.name, [(i.x, i.y) for i in points])

            persons_layer.add_to(self._map)

        buildings.add_to(self._map, index=-1)
        folium.LayerControl().add_to(self._map)
        self._map.show_in_browser()
