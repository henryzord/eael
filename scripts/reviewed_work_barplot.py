import argparse
import os

import numpy as np
from matplotlib import pyplot as plt, cm
from matplotlib.colors import to_hex
import matplotlib.patheffects as PathEffects


def main(output_path):
    fig, ax = plt.subplots(figsize=(7, 4))

    ax.set_xlim(-5, 105)
    ax.set_ylim(0, 5)

    labels = ['unavailable', 'not reviewed', 'wrong', 'original', 'duplicated']
    bars_y = [2.5]
    bars_x = [[12], [36], [11], [36], [5]]

    text_y = [1.75, 3.25, 1.75, 3.25, 1.75]

    colors = list(map(to_hex, cm.viridis(np.linspace(0.5, 1, len(labels)))))

    bars = []
    left = 0
    for i, x in enumerate(bars_x):
        bars += [ax.barh(bars_y, x, height=1, left=left, color=colors[i], label=labels[i])]

        text_x_label = (2 * left + x[0])/2 - (len(labels[i])/2 + 1)
        text_x_percentage = (2 * left + x[0])/2 - (len('{0}%'.format(x[0]))/2 + 1)

        percentage = ax.text(text_x_percentage, 2.45, '{0}%'.format(x[0]), fontdict=dict(color='black', weight='bold'))
        percentage.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])
        ax.text(text_x_label, 1.75, labels[i], fontdict=dict(color='black'))

        left += x[0]

    ax.annotate('reviewed', (79.3, 1.3), (74, 0.75),
                arrowprops=dict(arrowstyle='-[, widthB=8.65, lengthB=1.5', lw=1.0))

    # plt.legend(loc='upper right')

    plt.axis('off')
    plt.tight_layout()
    # plt.savefig(os.path.join(output_path, 'metadata_barplot.pdf'), format='pdf')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots a barplot with number of surveyed and non-surveyed work.')

    parser.add_argument(
        '--output-path', action='store', required=False,
        help='Path to folder where a PDF with the graph will be stored (if desired)'
    )

    args = parser.parse_args()
    main(output_path=args.output_path)
