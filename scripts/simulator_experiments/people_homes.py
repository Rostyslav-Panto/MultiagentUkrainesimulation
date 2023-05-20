import numpy as np
from matplotlib import pyplot as plt

import multiagentsimulator as ps


def plot_household_distribution() -> None:
    ps.init_globals()
    config = ps.sh.kyiv_config
    cr = ps.environment.interfaces.globals.registry
    assert cr

    ps.env.make_locations(config)
    ps.env.generate_population(config)

    retiree_homes_list = []
    minor_homes_list = []
    adult_homes_list = []

    homes = cr.location_ids_of_type(ps.env.Home)

    tot_persons = 0
    for home in homes:
        household = cr.get_persons_in_location(home)

        adults = 0
        minors = 0
        retirees = 0
        for member in household:
            if member.age <= 18:
                minors += 1
            elif 18 < member.age <= 65:
                adults += 1
            else:
                retirees += 1
        if minors > 0:
            minor_homes_list.append([minors, adults, retirees])
        elif adults > 0:
            adult_homes_list.append([minors, adults, retirees])
        elif retirees > 0:
            retiree_homes_list.append([minors, adults, retirees])
        tot_persons += len(household)

    minor_homes = np.asarray(minor_homes_list)
    adult_homes = np.asarray(adult_homes_list)
    retiree_homes = np.asarray(retiree_homes_list)

    n_rows = 2
    n_cols = 3
    plt.figure(figsize=(3 * n_cols, 3 * n_rows))
    plt_i = 0

    x = np.arange(3)
    colors = ['g', 'r', 'b']
    ylims = [0, max(np.max(minor_homes.sum(axis=0)), np.max(adult_homes.sum(axis=0)),
                    np.max(retiree_homes.sum(axis=0))) * 1.2]

    def plot_percent(n_homes: np.ndarray) -> None:
        for i, n in enumerate(n_homes):
            if n > 0:
                plt.text(i, n + 5, f'{n / config.num_persons * 100: 0.2f}%', ha="center", color=colors[i])

    plt_i += 1
    plt.subplot(n_rows, n_cols, plt_i)
    plt.bar(x, minor_homes.sum(axis=0), color=colors, alpha=0.5, width=0.3)
    plot_percent(minor_homes.sum(axis=0))
    plt.xticks(x, ['minors', 'adults', 'retirees'], fontsize=8)
    plt.title(f'{len(minor_homes)} Homes with children')
    plt.ylim(ylims)

    plt_i += 1
    plt.subplot(n_rows, n_cols, plt_i)
    plt.bar(x, adult_homes.sum(axis=0), color=colors, alpha=0.5, width=0.3)
    plot_percent(adult_homes.sum(axis=0))
    plt.xticks(x, ['minors', 'adults', 'retirees'], fontsize=8)
    plt.title(f'{len(adult_homes)} Homes with adults\n(no children)')
    plt.ylim(ylims)

    plt_i += 1
    plt.subplot(n_rows, n_cols, plt_i)
    plt.bar(x, retiree_homes.sum(axis=0), color=colors, alpha=0.5, width=0.3)
    retirees_in_nursing = sum(retiree_homes[:, 2])
    all_retirees = (sum(minor_homes[:, 2]) + sum(adult_homes[:, 2]) + sum(retiree_homes[:, 2]))
    plt.text(2, retirees_in_nursing + 7,
             f'{retirees_in_nursing / config.num_persons * 100: 0.2f}% (total-person)\n'
             f'{retirees_in_nursing / all_retirees * 100: 0.2f}% (total-retirees)',
             ha="right", color=colors[2])
    plt.xticks(x, ['minors', 'adults', 'retirees'], fontsize=8)
    plt.title(f'{len(retiree_homes)} Homes with only retirees')
    plt.ylim(ylims)

    plt_i += 1
    plt.subplot(n_rows, n_cols, plt_i)
    plt.hist(minor_homes[:, 0], [0, 1, 2, 3, 4], alpha=0.5, facecolor=colors[0], align='left', rwidth=0.3)
    plt.title(f'Children homes \n(avg Children/home: {minor_homes[:, 0].mean(): 0.2f})')
    plt.ylabel('num homes')
    plt.xlabel('minors')

    plt_i += 1
    plt.subplot(n_rows, n_cols, plt_i)
    nm = minor_homes[:, 1] + minor_homes[:, 2]
    plt.hist(nm, list(range(6)), alpha=0.5, facecolor=colors[1], align='left', rwidth=0.3)
    plt.title(f'Children homes \n(avg per home: {nm.mean(): 0.2f})')
    single_parent_homes = sum(nm == 1) / len(minor_homes)
    plt.text(1, sum(nm == 1) + 5, f'{single_parent_homes * 100: 0.2f}%\n(single-parent)', ha="center", color=colors[1])
    plt.ylabel('num homes')
    plt.xlabel('all adults (parents/relatives, retirees)')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_household_distribution()
