
from matplotlib import pyplot as plt

from multiagentsimulator.environment import ChosenRegulation, SimulationSettings
from multiagentsimulator.configs import EvaluationSettings, evaluate_strategies, make_evaluation_plots

if __name__ == '__main__':
    regulations = [
        ChosenRegulation(stay_home_if_sick=False, stage=0),
        ChosenRegulation(stay_home_if_sick=True, stage=1),
        ChosenRegulation(stay_home_if_sick=True, quarantine_if_contact_positive=True, stage=2)
    ]
    simulation_settings = {
        'Larger SICK': (0, SimulationSettings(random_testing_rate=0.3)),
        'CON 2': (0, SimulationSettings(use_contact_tracer=True, contact_tracer_history_size=2,
                                      random_testing_rate=0.3)),
        'CON 5': (0, SimulationSettings(use_contact_tracer=True, contact_tracer_history_size=5,
                                      random_testing_rate=0.3)),
        'CON 15': (0, SimulationSettings(use_contact_tracer=True, contact_tracer_history_size=15,
                                       random_testing_rate=0.3)),
    }
    param_labels, strategies, sim_opts = zip(*[(k, v[0], v[1]) for k, v in simulation_settings.items()])

    opts = EvaluationSettings(
        num_seeds=1,
        strategies=strategies,
        pandemic_regulations=regulations,
        sim_opts=sim_opts,  # type: ignore
    )

    experiment_name = 'trace_contacts'
    try:
        evaluate_strategies(experiment_name, opts)
    except ValueError:
        # Expect a value error because we are reusing the same directory.
        pass
    make_evaluation_plots(exp_name=experiment_name, data_saver_path=opts.data_saver_path, param_labels=param_labels,
                          bar_plot_xlabel='Contact Tracing', show_cumulative_reward=False, annotate_stages=False)
    plt.show()
