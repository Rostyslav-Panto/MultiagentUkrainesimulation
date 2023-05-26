from tqdm import trange

import multiagentsimulator as ms


def run_pandemic_sim() -> None:
    ms.init_globals(seed=1)
    sim_config = ms.sh.kyiv_config

    sim = ms.env.Simulator.from_config(sim_config, map_on=True)

    viz = ms.visualization.MapViz(
        locations=sim.locations,
        city=sim_config.city,
    )

    sim.impose_regulation(regulation=ms.sh.ukraine_regulations[0])  # stage 0
    for _ in trange(10, desc='Simulating day'):
        sim.step_day()
        viz.record_state(sim.state)

    viz.plot()


if __name__ == '__main__':
    run_pandemic_sim()
