from tqdm import trange

import multiagentsimulator as ms
from multiagentsimulator.environment import SimulationSettings


def run_pandemic_sim() -> None:
    ms.init_globals(seed=1)
    sim_config = ms.sh.kyiv_config

    sim = ms.env.Simulator.from_config(
        sim_config,
        sim_opts=SimulationSettings(contact_tracer_history_size=5),
        map_on=True)

    viz = ms.visualization.MapViz(
        locations=sim.locations,
        city=sim_config.city,
    )
    viz2 = ms.visualization.SimViz.from_config(sim_config)

    sim.impose_regulation(regulation=ms.sh.ukraine_regulations[0])  # stage 0
    for _ in trange(100, desc='Simulating day'):
        sim.step_day()
        # viz.record_state(sim.state)
        viz2.record_state(sim.state)

    viz2.plot()
    # viz.plot()


if __name__ == '__main__':
    run_pandemic_sim()
