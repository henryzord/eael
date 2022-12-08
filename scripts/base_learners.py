# encoding=utf-8

"""
Script for generating figure which groups work in the survey by base classifier used.
"""

import argparse
import os

import numpy as np
import pandas as pd
import seaborn
from matplotlib import cm
from matplotlib import pyplot as plt

try:
    from scripts import load_data
except ImportError:
    from __init__ import load_data

seaborn.set()


def plot_base_learners(tables, output_path=None):
    colors = cm.viridis(np.linspace(0, 1, num=6)[3:])

    fig, ax = plt.subplots(figsize=(7, 6))

    dfa = tables['base learner type']  # type: pd.DataFrame
    dfb = tables['base learner distribution']  # type: pd.DataFrame

    # only gets algorithms that appeared in more than 5 work
    dfa = dfa.loc[:, dfa.sum(axis=0) >= 5]
    dfb = dfb.loc[[x in dfa.index for x in dfb.index]]

    bar_height = 1.75  # the width of the bars: can also be len(x) sequence
    y_tick_labels = dfa.columns.tolist()

    N = len(y_tick_labels)
    y_ticks = np.arange(0, N * 4, 4)  # the x locations for the groups

    fontsize = 12

    dist_columns = ['homogeneous', 'heterogeneous']

    ps = []
    # iterates over distributions: homogeneous, heterogeneous and both
    way = -1
    for color, dist in zip(colors, dist_columns):
        dist_loc = dfb.loc[dfb[dist] | dfb['both']]

        intersects = []
        for algorithm in dfa.columns:  # iterates over base learners
            algorithm_loc = dfa.loc[dfa[algorithm]]

            intersects += [len(dist_loc.join(algorithm_loc, how='inner'))]

        ps += [ax.barh(y=y_ticks, width=way * np.array(intersects), height=bar_height, color=color, align='center')]

        for x_tick, y_tick in zip(intersects, y_ticks):
            if x_tick > 0:
                ax.text(x_tick * way + (-4.5 if way < 0 else 1), y_tick - 0.75, '%2.d' % x_tick, fontdict=dict(size=fontsize))

        way *= -1

    for y_tick, label in zip(y_ticks, y_tick_labels):
        ax.text(-len(label)/2 - 3.75, y_tick + 1.2, label, fontdict=dict(size=fontsize, color='black', weight='normal'))  

    ax.set_ylim(-3.5 + y_ticks[0], y_ticks[-1] + 2)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.8])

    ax.legend(
        tuple(map(lambda x: x[0], ps)), dist_columns,
        loc='upper center', bbox_to_anchor=(0.5, 0.059), fontsize=fontsize, ncol=2
    )

    ax.set_axis_off()
    plt.show()

    if output_path is not None:
        fig.savefig(
            os.path.join(output_path, 'figures_base_learners_distribution.pdf'),
            format='pdf',
            orientation='landscape'
        )


def main(data_path, output_path):
    tables = load_data(data_path)
    plot_base_learners(tables, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script for generating bar plot of surveyed work vs base learner employed.'
    )
    parser.add_argument(
        '--data', action='store', required=True,
        help='Path to .json file with all citation references'
    )
    parser.add_argument(
        '--output-path', action='store', required=False,
        help='Path to folder where a PDF with the graph will be stored (if desired)'
    )
    args = parser.parse_args()
    main(data_path=args.data, output_path=args.output_path)
