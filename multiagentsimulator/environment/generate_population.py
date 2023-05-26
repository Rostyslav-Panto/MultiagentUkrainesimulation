from typing import List, cast
from uuid import uuid4

import numpy as np

from . import University
from .interfaces import globals, Risk, Person, PersonID, PersonState, BusinessBaseLocation
from .job_counselor import JobCounselor
from .location import Home, School
from .person import Retired, Adult, Child
from .person.student import Student
from .simulator_config import SimulationConfigs
from ..utils import cluster_into_random_sized_groups

age_group = range(2, 101)


def get_ukraine_age_distribution(num_persons: int) -> List[int]:
    age_p = np.zeros(100)
    for i, age in enumerate(age_group):
        if age < 60:
            age_p[i] = globals.numpy_rng.normal(1, 0.05)
        else:
            age_p[i] = (1 + (age - 60) * (0.05 - 1) / (100 - 60)) * globals.numpy_rng.normal(1, 0.05)
    age_p /= np.sum(age_p)
    ages = [int(globals.numpy_rng.choice(np.arange(1, 101), p=age_p)) for _ in range(num_persons)]
    return ages


def infection_risk(age: int) -> Risk:
    return cast(Risk,
                globals.numpy_rng.choice([Risk.LOW, Risk.HIGH], p=[1 - age / age_group.stop, age / age_group.stop]))


def generate_population(sim_config: SimulationConfigs) -> List[Person]:
    assert globals.registry, 'No registry found. Create the repo wide registry first by calling init_globals()'
    registry = globals.registry
    numpy_rng = globals.numpy_rng

    persons: List[Person] = []

    ages = get_ukraine_age_distribution(sim_config.num_persons)
    numpy_rng.shuffle(ages)
    minor_ages = []
    student_ages = []
    adult_ages = []
    retiree_ages = []

    for unsorted_age in ages:
        if unsorted_age <= 18:
            minor_ages.append(unsorted_age)
        elif 18 < unsorted_age <= 21:
            student_ages.append(unsorted_age)
        elif 21 < unsorted_age <= 65:
            adult_ages.append(unsorted_age)
        else:
            retiree_ages.append(unsorted_age)

    all_homes = list(registry.location_ids_of_type(Home))
    numpy_rng.shuffle(all_homes)
    unlived_homes = all_homes

    num_of_sick_retirees = np.ceil(len(retiree_ages) * 0.065).astype('int')
    retirees_in_nursing_ages = retiree_ages[:num_of_sick_retirees]
    clustered_nursing_ages = cluster_into_random_sized_groups(retirees_in_nursing_ages, 1, 2, numpy_rng)
    retiree_homes_ages = [(unlived_homes[_i], _a) for _i, _g in enumerate(clustered_nursing_ages) for _a in _g]
    nursing_homes = unlived_homes[:len(clustered_nursing_ages)]
    unlived_homes = unlived_homes[len(nursing_homes):]
    unassigned_retiree_ages = retiree_ages[num_of_sick_retirees:]

    for home, retiree_age in retiree_homes_ages:
        persons.append(Retired(person_id=PersonID(f'retired_{str(uuid4())}', retiree_age),
                               home=home,
                               regulation_compliance_prob=sim_config.regulation_compliance_prob,
                               init_state=PersonState(current_location=home, risk=infection_risk(retiree_age))))

    schools = registry.location_ids_of_type(School)
    clustered_minor_ages = cluster_into_random_sized_groups(minor_ages, 1, 3, numpy_rng)
    assert len(unlived_homes) >= len(clustered_minor_ages), 'not enough homes to assign all people'

    minor_homes_ages = [(unlived_homes[_i], _a) for _i, _g in enumerate(clustered_minor_ages) for _a in _g]
    minor_homes = unlived_homes[:len(clustered_minor_ages)]
    unlived_homes = unlived_homes[len(minor_homes):]
    # create all minor
    for home, minor_age in minor_homes_ages:
        persons.append(Child(person_id=PersonID(f'minor_{str(uuid4())}', minor_age),
                             home=home,
                             school=numpy_rng.choice(schools) if len(schools) > 0 else None,
                             regulation_compliance_prob=sim_config.regulation_compliance_prob,
                             init_state=PersonState(current_location=home, risk=infection_risk(minor_age))))

    universities = registry.location_ids_of_type(University)
    clustered_student_ages = cluster_into_random_sized_groups(student_ages, 1, 3, numpy_rng)
    assert len(unlived_homes) >= len(clustered_student_ages), 'not enough homes to assign all people'

    student_homes_ages = [(unlived_homes[_i], _a) for _i, _g in enumerate(clustered_student_ages) for _a in _g]
    student_homes = unlived_homes[:len(clustered_student_ages)]
    unlived_homes = unlived_homes[len(student_homes):]

    for home, student_age in student_homes_ages:
        persons.append(Student(person_id=PersonID(f'student_{str(uuid4())}', student_age),
                             home=home,
                             university=numpy_rng.choice(universities) if len(universities) > 0 else None,
                             regulation_compliance_prob=sim_config.regulation_compliance_prob,
                             init_state=PersonState(current_location=home, risk=infection_risk(student_age))))

    required_num_adults = len(minor_homes) + len(student_homes) + len(unlived_homes) - len(unassigned_retiree_ages)
    assert len(adult_ages) >= required_num_adults, (
        f'not enough adults {required_num_adults} to ensure each minor home has at least a single '
        f'adult and all the homes are filled.')
    adult_homes_ages = [(_h, adult_ages[_i]) for _i, _h in enumerate(minor_homes)]
    non_nursing_homes_ages = []

    minor_homes.extend(student_homes)
    non_single_parent_minor_homes = minor_homes[int(len(minor_homes) * 0.23):]
    homes_to_distribute = unlived_homes + non_single_parent_minor_homes
    numpy_rng.shuffle(homes_to_distribute)
    unassigned_adult_ages = adult_ages[len(minor_homes):]
    for i in range(len(unassigned_retiree_ages) + len(unassigned_adult_ages)):
        home = homes_to_distribute[i % len(homes_to_distribute)]
        if len(unassigned_retiree_ages) > 0:
            age = unassigned_retiree_ages.pop(0)
            non_nursing_homes_ages.append((home, age))
        else:
            age = unassigned_adult_ages.pop(0)
            adult_homes_ages.append((home, age))

    work_ids = registry.location_ids_of_type(BusinessBaseLocation)
    assert len(work_ids) > 0, 'no business locations found!'
    for home, age in adult_homes_ages:
        job_counselor = JobCounselor(sim_config.location_configs)
        work_package = job_counselor.next_available_work()
        assert work_package, 'Not enough available jobs, increase the capacity of certain businesses'
        persons.append(Adult(person_id=PersonID(f'worker_{str(uuid4())}', age),
                             home=home,
                             work=work_package.work,
                             work_time=work_package.work_time,
                             regulation_compliance_prob=sim_config.regulation_compliance_prob,
                             init_state=PersonState(current_location=home, risk=infection_risk(age))))

    for home, age in non_nursing_homes_ages:
        persons.append(Retired(person_id=PersonID(f'retired_{str(uuid4())}', age),
                               home=home,
                               regulation_compliance_prob=sim_config.regulation_compliance_prob,
                               init_state=PersonState(current_location=home, risk=infection_risk(age))))

    return persons
