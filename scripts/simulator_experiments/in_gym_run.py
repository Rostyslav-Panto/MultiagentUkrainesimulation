from tqdm import trange

import multiagentsimulator as ps


def run_pandemic_gym_env() -> None:

    # init globals
    ps.init_globals(seed=0)

    # select a simulator config
    sim_config = ps.sh.kyiv_config

    # make env
    env = ps.env.GymEnvironment.from_config(sim_config, pandemic_regulations=ps.sh.ukraine_regulations)

    # setup viz
    viz = ps.visualization.GymViz.from_config(sim_config=sim_config)

    # run stage-0 action steps in the environment
    env.reset()
    for _ in trange(100, desc='Simulating day'):
        obs, reward, done, aux = env.step(action=0)
        viz.record((obs, reward))

    viz.plot()


if __name__ == '__main__':
    run_pandemic_gym_env()