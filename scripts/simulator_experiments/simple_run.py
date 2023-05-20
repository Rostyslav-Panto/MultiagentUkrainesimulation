from tqdm import trange

import multiagentsimulator as ps


def run_pandemic_sim() -> None:

    # init globals
    ps.init_globals(seed=1)

    # select a simulator config
    sim_config = ps.sh.kyiv_config

    # make sim
    sim = ps.env.Simulator.from_config(sim_config)

    # setup viz to show plots
    viz = ps.visualization.SimViz.from_config(sim_config)

    # impose a regulation
    sim.impose_regulation(regulation=ps.sh.austin_regulations[0])  # stage 0

    # run regulation steps in the simulator
    for _ in trange(100, desc='Simulating day'):
        sim.step_day()
        viz.record(sim.state)

    # generate plots
    viz.plot()


if __name__ == '__main__':
    run_pandemic_sim()
