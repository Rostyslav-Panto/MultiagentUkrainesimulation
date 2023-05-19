from tqdm import trange

import multiagentsimulator as ps

# the first thing to do at the start of any experiment is to initialize a few global parameters
ps.init_globals() # you can pass parameters, like a random seed, that are shared across the entire repo.

# init locations
home = ps.env.Home()
work = ps.env.Office()

# init a worker
person = ps.env.Adult(
    person_id=ps.env.PersonID('worker', age=35),  # person_id is a unique id for this person
    home=home.id,  # specify the home_id that person is assigned to
    work=work.id,  # specify the id of the person's workplace
)

# init simulator
sim = ps.env.Simulator(locations=[work, home], persons=[person])

# iterate through steps in the simulator, where each step advances an hour
for _ in trange(24, desc='Simulating hour'):
    sim.step()
    print(sim.registry.person_ids)
