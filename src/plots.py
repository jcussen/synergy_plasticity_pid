"""
This file contains plotting functions to create results figures.
"""

import os
import matplotlib.pyplot as plt
from src.util import (
    col_labels,
    plot_colours,
)


def plot_pid(data, k, pw, output_dir):
    """plots raw PID values (in bits) with standard deviation error bars"""
    # create dir if doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
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


def plot_sig(data, k, pw, output_dir, p_value=0.05):
    """plots normalised PID values and checks significance"""
    # create dir if doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = str(output_dir) + f"/sig_k{str(k)}_pw{str(pw)}"
    col_dict = col_labels.get(k).get(pw)
    fig, ax = plt.subplots()
    df = data[data["pathway"] == pw]
    df = df[df["k_condition"] == k]
    cols = list(col_dict.keys())
    colours = plot_colours
    for i, mean_col in enumerate(cols):
        if mean_col != "mi_mean":
            p_col = mean_col.replace("mean", "p")
            df_sig = df[df[p_col] < p_value]
            df_nonsig = df[df[p_col] >= p_value]
            ax.errorbar(
                x=df["learning_time"],
                y=df[mean_col],
                label=col_dict.get(mean_col),
                color=colours[i],
                zorder=1,
            )
            if i == 0:  # include label for first plot
                ax.scatter(
                    x=df_sig["learning_time"],
                    y=df_sig[mean_col],
                    marker="o",
                    zorder=2,
                    label="Significant",
                    facecolors="none",
                    edgecolors="grey",
                )
                ax.scatter(
                    x=df_nonsig["learning_time"],
                    y=df_nonsig[mean_col],
                    marker="x",
                    zorder=2,
                    label="Non-significant",
                    color="grey",
                )
            else:
                ax.scatter(
                    x=df_sig["learning_time"],
                    y=df_sig[mean_col],
                    marker="o",
                    zorder=2,
                    facecolors="none",
                    edgecolors="grey",
                )
                ax.scatter(
                    x=df_nonsig["learning_time"],
                    y=df_nonsig[mean_col],
                    marker="x",
                    zorder=2,
                    color="grey",
                )
    ax.legend()
    ax.set_ylabel("Normalised information")
    ax.set_xlabel("Time (mins)")
    plt.ylim(top=1)
    plt.savefig(output_path, bbox_inches="tight")
    plt.show()
