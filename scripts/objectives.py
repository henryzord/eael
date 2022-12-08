# encoding=utf-8

"""
For documentation please refer to https://github.com/konstantint/matplotlib-venn
"""

import argparse
import os

import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_circles
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

from scripts import load_data


def plot_venn_diagram(tables, output_path):
    fig, ax = plt.subplots(figsize=(7, 4))

    colors = cm.viridis(np.arange(0, 1, 0.1))

    df = tables['objective']

    mf = df.loc[
        df[('multi', 'effectiveness')] |
        df[('multi', 'efficiency')] |
        df[('multi', 'diversity')] |
        df[('multi', 'complexity')]
    ]

    subsets = (
        # only efficiency
        mf.loc[mf[('multi', 'efficiency')] & ~mf[('multi', 'diversity')] & ~mf[('multi', 'complexity')]].shape[0],
        # only diversity
        mf.loc[~mf[('multi', 'efficiency')] & mf[('multi', 'diversity')] & ~mf[('multi', 'complexity')]].shape[0],
        # efficiency ^ diversity
        mf.loc[mf[('multi', 'efficiency')] & mf[('multi', 'diversity')]].shape[0],
        # only complexity
        mf.loc[~mf[('multi', 'efficiency')] & ~mf[('multi', 'diversity')] & mf[('multi', 'complexity')]].shape[0],
        # complexity ^ efficiency
        mf.loc[mf[('multi', 'complexity')] & mf[('multi', 'efficiency')]].shape[0],
        # complexity ^ diversity
        mf.loc[mf[('multi', 'complexity')] & mf[('multi', 'diversity')]].shape[0],
        # efficiency ^ diversity ^ complexity
        mf.loc[mf[('multi', 'efficiency')] & mf[('multi', 'diversity')] & mf[('multi', 'complexity')]].shape[0],
    )

    venn_colors = [
        colors[8],  # efficiency
        colors[8],  # diversity
        colors[6],  # efficiency ^ diversity
        colors[8],  # complexity
        colors[6],  # complexity ^ efficiency
        colors[6],  # complexity ^ diversity
        colors[4]   # efficiency ^ diversity ^ complexity
    ]

    codes = [
        '100',  # efficiency
        '010',  # diversity
        '110',  # efficiency ^ diversity
        '001',  # complexity
        '101',  # complexity ^ efficiency
        '011',  # complexity ^ diversity
        '111'   # efficiency ^ diversity ^ complexity
    ]

    patches = []

    # add a fancy box
    patches += [mpatches.FancyBboxPatch(
        xy=(-1.5, -0.5), width=3, height=1,
        boxstyle=mpatches.BoxStyle("Round", pad=0.02),
        edgecolor='black', linewidth=3.
    )]

    plt.text(-0.825, 0.45, 'effectiveness (%d)' % len(mf), fontdict=dict(size=12))

    collection = PatchCollection(patches, alpha=0.3)
    collection.set_color('white')
    ax.add_collection(collection)

    v = venn3(
        subsets=subsets,
        set_labels=('efficiency', 'diversity', 'complexity'),
        set_colors=[colors[0], colors[4], colors[8]]
    )

    c = venn3_circles(subsets=subsets, linestyle='solid', linewidth=0.8)

    for code, color in zip(codes, venn_colors):
        patch = v.get_patch_by_id(code)
        if patch is not None:
            patch.set_color(color)

    plt.axis('on')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'objective_venn_diagram.pdf'), format='pdf')
    plt.show()


def main(data_path, output_path):
    tables = load_data(data_path)
    plot_venn_diagram(tables, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for generating venn diagram for paper.')
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
