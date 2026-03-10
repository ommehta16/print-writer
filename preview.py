"""
preview.py

Renders a matplotlib preview of pen-down strokes only.

Usage:
    from preview import preview_paths
    preview_paths(paths)
    preview_paths(paths, save='preview.png')
"""

import matplotlib.pyplot as plt
from pen_config import CONFIG


def preview_paths(paths, save=None, show=True):
    pw = CONFIG['page_width']
    ph = CONFIG['page_height']

    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_facecolor('white')

    for path in paths:
        points = list(path)
        if not points:
            continue
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.plot(xs, ys, color='black', linewidth=0.8)

    ax.set_xlim(0, pw)
    ax.set_ylim(0, ph)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=150)
        print(f'Saved preview to {save}')

    if show:
        plt.show()

    return fig, ax


# --- Example / test ---
if __name__ == '__main__':
    square = [(10, 10), (50, 10), (50, 50), (10, 50), (10, 10)]
    cross  = [(10, 10), (50, 50), (30, 30), (50, 10), (10, 50)]

    preview_paths([square, cross], save='preview.png', show=False)
