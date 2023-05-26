from typing import List

from ..environment import ChosenRegulation, DEFAULT, Risk, Office, School, University, Restaurant

ukraine_regulations: List[ChosenRegulation] = [
    ChosenRegulation(stay_home_if_sick=False,
                     practice_good_hygiene=False,
                     wear_facial_coverings=False,
                     social_distancing=DEFAULT,
                     risk_to_avoid_gathering_size={Risk.LOW: -1, Risk.HIGH: -1},
                     location_type_to_rule_kwargs={
                           Office: {'lock': False},
                           School: {'lock': False},
                           University: {'lock': False},
                           Restaurant: {'lock': False},
                       },
                     stage=0),
    ChosenRegulation(stay_home_if_sick=True,
                     practice_good_hygiene=True,
                     wear_facial_coverings=False,
                     social_distancing=0.2,
                     location_type_to_rule_kwargs={
                           Office: {'lock': False},
                           School: {'lock': False},
                           University: {'lock': False},
                           Restaurant: {'lock': False},
                       },
                     stage=1),
    ChosenRegulation(stay_home_if_sick=True,
                     practice_good_hygiene=True,
                     wear_facial_coverings=False,
                     social_distancing=0.25,
                     location_type_to_rule_kwargs={
                           Office: {'lock': False},
                           School: {'lock': True},
                           University: {'lock': False},
                           Restaurant: {'lock': False},
                       },
                     stage=2),
    ChosenRegulation(stay_home_if_sick=True,
                     practice_good_hygiene=True,
                     wear_facial_coverings=True,
                     social_distancing=0.6,
                     risk_to_avoid_gathering_size={Risk.HIGH: 0, Risk.LOW: 0},
                     location_type_to_rule_kwargs={
                           Office: {'lock': False},
                           School: {'lock': True},
                           University: {'lock': True},
                           Restaurant: {'lock': True},
                       },
                     stage=3),
    ChosenRegulation(stay_home_if_sick=True,
                     practice_good_hygiene=True,
                     wear_facial_coverings=True,
                     social_distancing=0.8,
                     risk_to_avoid_gathering_size={Risk.HIGH: 0, Risk.LOW: 0},
                     location_type_to_rule_kwargs={
                           Office: {'lock': True},
                           School: {'lock': True},
                           University: {'lock': True},
                           Restaurant: {'lock': True},
                       },
                     stage=4)
]

# https://home.kpmg/xx/en/home/insights/2020/04/sweden-government-and-institution-measures-in-response-to-covid.html
# Sweden took no nationwide lockdown; Remote work *recommended*;
# Schools are open; Restaurants are open.
# Travel ban.

# https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/communicable-disease-control/covid-19/prevention/
# We do not currently recommend face masks in public settings since the scientific evidence
# around the effectiveness of face masks in combatting the spread of infection is unclear.
# https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/communicable-disease-control/
# covid-19--the-swedish-strategy/

# Anders Tegnell says his modelling indicates that, on average, Swedes have around 30% of the social interactions they
# did prior to the pandemic.

static_regulations: List[ChosenRegulation] = [
    ChosenRegulation(stay_home_if_sick=False,
                     practice_good_hygiene=False,
                     wear_facial_coverings=False,
                     social_distancing=DEFAULT,
                     risk_to_avoid_gathering_size={Risk.LOW: -1, Risk.HIGH: -1},
                     location_type_to_rule_kwargs={
                           Office: {'lock': False},
                           School: {'lock': False},
                           University: {'lock': False},
                           Restaurant: {'lock': False},
                       },
                     stage=0),
    ChosenRegulation(stay_home_if_sick=True,
                     practice_good_hygiene=True,
                     social_distancing=0.139,  # after calibration
                     risk_to_avoid_gathering_size={Risk.HIGH: 50, Risk.LOW: 50},
                     stage=1),
]
