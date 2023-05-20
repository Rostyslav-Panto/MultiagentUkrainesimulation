import geopandas
import folium
from folium import Circle

from multiagentsimulator.data.city_buildings.city import City

city = City(distance=2000)
city_map = city.get_map()
city_buildings = city.get_classified_buildings_in_distance()
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',"grey"]
locs_map = []
for name, buildings, color in zip(
        city_buildings.keys(),
        city_buildings.values(),
        colors):
    print(f"{name}:", len(buildings))
    for _, r in buildings.iterrows():
        sim_geo = geopandas.GeoSeries(r["geometry"])
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(
            name=name,
            data=geo_j,
            style_function=lambda feature, col=color: {'fillColor': col,
                                            'color': col,
                                            'fillOpacity': 0.5,
                                            },
        marker=Circle(radius=0))
        locs_map.append(geo_j)
for i in locs_map:
    i.add_to(city_map)
# folium.(city_map)
city_map.show_in_browser()
