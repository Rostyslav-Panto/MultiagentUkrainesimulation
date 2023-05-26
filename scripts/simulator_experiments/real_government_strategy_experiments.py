
from matplotlib import pyplot as plt

import multiagentsimulator as ps


def eval_government_strategies(experiment_name: str, opts: ps.sh.EvaluationSettings) -> None:
    data_saver = ps.data.H5DataSaver(experiment_name, path=opts.data_saver_path)
    print('Running Static strategy')
    ps.sh.experiment_main(sim_config=opts.default_sim_config,
                          sim_opts=ps.env.SimulationSettings(),
                          data_saver=data_saver,
                          pandemic_regulations=ps.sh.static_regulations,
                          stages_to_execute=static_strategy,
                          num_random_seeds=opts.num_seeds,
                          max_episode_length=opts.max_episode_length,
                          exp_id=0)

    print('Running Ukraine strategy')
    ps.sh.experiment_main(sim_config=opts.default_sim_config,
                          sim_opts=ps.env.SimulationSettings(),
                          data_saver=data_saver,
                          pandemic_regulations=ps.sh.ukraine_regulations,
                          stages_to_execute=ukraine_strategy,
                          num_random_seeds=opts.num_seeds,
                          max_episode_length=opts.max_episode_length,
                          exp_id=1)


if __name__ == '__main__':
    static_strategy = [ps.data.StageSchedule(stage=0, end_day=3),
                       ps.data.StageSchedule(stage=1, end_day=None)]
    ukraine_strategy = [ps.data.StageSchedule(stage=0, end_day=3),
                        ps.data.StageSchedule(stage=1, end_day=8),
                        ps.data.StageSchedule(stage=2, end_day=13),
                        ps.data.StageSchedule(stage=3, end_day=25),
                        ps.data.StageSchedule(stage=4, end_day=59),
                        ps.data.StageSchedule(stage=3, end_day=79),
                        ps.data.StageSchedule(stage=2, end_day=None)]

    opts = ps.sh.EvaluationSettings(
        num_seeds=30,
        max_episode_length=180,
        enable_warm_up=False
    )

    exp_name = 'ukraine_and_static_strategies'
    try:
        eval_government_strategies(exp_name, opts)
    except ValueError:
        pass
    ps.sh.make_evaluation_plots(exp_name=exp_name,
                                data_saver_path=opts.data_saver_path,
                                param_labels=['STAT', 'UKR'],
                                bar_plot_xlabel='Real Government Strategies',
                                annotate_stages=True,
                                show_cumulative_reward=False,
                                show_time_to_peak=False, show_pandemic_duration=True)
    plt.show()
