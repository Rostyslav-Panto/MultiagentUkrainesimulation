
from .person_routines import DefaultPersonRoutineAssignment
from ..environment import Home, GroceryStore, Office, School, Hospital, RetailStore, University, Restaurant, Bar, \
    SimulationConfigs, LocationConfigs


"""
A few references for the numbers selected:

http://www.worldcitiescultureforum.com/data/number-of-restaurants-per-100.000-population (Austin)

"""

town_config = SimulationConfigs(
    num_persons=10000,
    location_configs=[
        LocationConfigs(Home, num=3000),
        LocationConfigs(GroceryStore, num=40, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=50, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=100, num_assignees=4, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=10, num_assignees=30, state_opts=dict(patient_capacity=10)),
        LocationConfigs(RetailStore, num=40, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(University, num=40, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=20, num_assignees=6, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Bar, num=20, num_assignees=5, state_opts=dict(visitor_capacity=30)),
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

above_medium_town_config = SimulationConfigs(
    num_persons=4000,
    location_configs=[
        LocationConfigs(Home, num=1200),
        LocationConfigs(GroceryStore, num=16, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=20, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=40, num_assignees=4, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=4, num_assignees=30, state_opts=dict(patient_capacity=10)),
        LocationConfigs(RetailStore, num=16, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(University, num=16, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=8, num_assignees=6, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Bar, num=8, num_assignees=4, state_opts=dict(visitor_capacity=30))
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

medium_town_config = SimulationConfigs(
    num_persons=2000,
    location_configs=[
        LocationConfigs(Home, num=600),
        LocationConfigs(GroceryStore, num=8, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=10, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=20, num_assignees=4, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=2, num_assignees=30, state_opts=dict(patient_capacity=10)),
        LocationConfigs(RetailStore, num=8, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(University, num=8, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=4, num_assignees=6, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Bar, num=4, num_assignees=3, state_opts=dict(visitor_capacity=30))
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

small_town_config = SimulationConfigs(
    num_persons=1000,
    location_configs=[
        LocationConfigs(Home, num=300),
        LocationConfigs(GroceryStore, num=4, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=5, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=10, num_assignees=4, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=1, num_assignees=30, state_opts=dict(patient_capacity=10)),
        LocationConfigs(RetailStore, num=4, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(University, num=4, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=2, num_assignees=6, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Bar, num=2, num_assignees=5, state_opts=dict(visitor_capacity=30)),
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

tiny_town_config = SimulationConfigs(
    num_persons=500,
    location_configs=[
        LocationConfigs(Home, num=150),
        LocationConfigs(GroceryStore, num=2, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=2, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=10, num_assignees=2, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=1, num_assignees=15, state_opts=dict(patient_capacity=5)),
        LocationConfigs(RetailStore, num=2, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(University, num=2, num_assignees=3, state_opts=dict(visitor_capacity=5)),
        LocationConfigs(Restaurant, num=1, num_assignees=6, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Bar, num=1, num_assignees=3, state_opts=dict(visitor_capacity=30))
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

test_config = SimulationConfigs(
    num_persons=100,
    location_configs=[
        LocationConfigs(Home, num=30),
        LocationConfigs(GroceryStore, num=1, num_assignees=5, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Office, num=1, num_assignees=150, state_opts=dict(visitor_capacity=0)),
        LocationConfigs(School, num=10, num_assignees=2, state_opts=dict(visitor_capacity=30)),
        LocationConfigs(Hospital, num=1, num_assignees=30, state_opts=dict(patient_capacity=2)),
        LocationConfigs(Restaurant, num=1, num_assignees=3, state_opts=dict(visitor_capacity=10)),
        LocationConfigs(Bar, num=1, num_assignees=3, state_opts=dict(visitor_capacity=10)),
    ],
    person_routine_assignment=DefaultPersonRoutineAssignment())

