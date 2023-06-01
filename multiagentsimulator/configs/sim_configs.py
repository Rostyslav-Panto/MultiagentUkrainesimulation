from .person_routines import DefaultPersonRoutineAssignment
from ..data.city_buildings.city import City
from ..environment import Home, Store, Office, School, Hospital, University, Restaurant, \
    SimulationConfigs, LocationConfigs

medium_town_config = SimulationConfigs(
    num_persons=2000,
    location_configs=[
        LocationConfigs(Home, num=600),
        LocationConfigs(Store, num=8, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=10, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=20, num_assignees=4, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=2, num_assignees=30, state_opts=dict(patient_capacity=10)),
        LocationConfigs(University, num=8, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=4, num_assignees=6, state_opts=dict(visitor_capacity=30)),
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

small_town_config = SimulationConfigs(
    num_persons=1000,
    location_configs=[
        LocationConfigs(Home, num=300),
        LocationConfigs(Store, num=4, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=5, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=10, num_assignees=4, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=1, num_assignees=30, state_opts=dict(patient_capacity=10)),
        LocationConfigs(University, num=4, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=2, num_assignees=6, state_opts=dict(visitor_capacity=30)),
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())


def get_kyiv_configs():
    city = City(distance=5000)
    buildings = city.get_classified_buildings_in_distance()
    homes = buildings["Home"]
    stores = buildings["Store"]
    offices = buildings["Office"]
    schools = buildings["School"]
    hospitals = buildings["Hospital"]
    restaurants = buildings["Restaurant"]
    universities = buildings["University"]
    return [
        LocationConfigs(Home, num=len(homes), positions=homes),
        LocationConfigs(Store, num=len(stores), num_assignees=5, state_opts=dict(visitor_capacity=150),
                        positions=homes),
        LocationConfigs(Office, num=len(offices), num_assignees=150, state_opts=dict(visitor_capacity=100),
                        positions=stores),
        LocationConfigs(School, num=len(schools), num_assignees=2, state_opts=dict(visitor_capacity=300),
                        positions=schools),
        LocationConfigs(Hospital, num=len(hospitals), num_assignees=30, state_opts=dict(patient_capacity=500),
                        positions=hospitals),
        LocationConfigs(Restaurant, num=len(restaurants), num_assignees=3, state_opts=dict(visitor_capacity=10),
                        positions=restaurants),
        LocationConfigs(University, num=len(universities), num_assignees=250, state_opts=dict(visitor_capacity=250),
                        positions=universities),
    ]


class KyivSimConfigs(SimulationConfigs):
    def __init__(self, num_persons, location_configs, person_routine_assignment):
        super().__init__(
            num_persons=num_persons,
            location_configs=location_configs,
            person_routine_assignment=person_routine_assignment
        )
        self.city = City(distance=5000)
        self.buildings = self.city.get_classified_buildings_in_distance()


kyiv_config = KyivSimConfigs(
    num_persons=10000,
    location_configs=get_kyiv_configs(),
    person_routine_assignment=DefaultPersonRoutineAssignment())

