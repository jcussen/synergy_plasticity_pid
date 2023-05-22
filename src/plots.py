"""
This file contains plotting functions to create results figures.
"""

import matplotlib.pyplot as plt
from src.util import (
    col_labels,
    plot_colours,
)


def plot_pid(data, k, pw, output_dir):
    """plots raw PID values (in bits) with standard deviation error bars"""
    output_path = str(output_dir) + f"/pid_k{str(k)}_pw{str(pw)}"
    col_dict = col_labels.get(k).get(pw)
    fig, ax = plt.subplots()
    df = data[data["pathway"] == pw]
    df = df[df["k_condition"] == k]
    cols = list(col_dict.keys())
    colours = plot_colours
    for i, mean_col in enumerate(cols):
        std_col = mean_col.replace("mean", "std")
        ax.errorbar(
            x=df["learning_time"],
            y=df[mean_col],
            yerr=df[std_col],
            label=col_dict.get(mean_col),
            color=colours[i],
            ecolor="black",
            capsize=2,
        )
    ax.legend()
    ax.set_ylabel("Bits")
    ax.set_xlabel("Time (mins)")
    plt.savefig(output_path, bbox_inches="tight")
    plt.show()
