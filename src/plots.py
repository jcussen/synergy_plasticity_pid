import os
import matplotlib.pyplot as plt
import pandas as pd

from src.util import (
    figures_dir,
    results_dir,
    condition_cols,
    pid_value_cols,
    schemes,
    col_labels,
    plot_colours,
)


def plot_pid(data, k, pw, output_dir):
    """plots raw PID values (in bits) with standard deviation error bars"""
    output_path = str(output_dir) + f"/pid_{str(k)}_{str(pw)}"
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


#%%
# condition = 'Hebbian_antiHebbian'
#
# dir = os.path.join(figures_dir, condition)
# results = os.path.join(results_dir, condition)
# data = pd.read_feather(os.path.join(results, 'final_results_phasic'))
#
# if not os.path.exists(dir):
#     os.makedirs(dir)
# plot_err_bar(data, col_labels, 1, 9, dir)

#%% fix col names
#
# for condition in schemes:
#     for phasic_name in ['phasic', 'tonic']:
#         dir = os.path.join(results_dir, condition)
#         pid = pd.read_feather(
#             os.path.join(dir, f"trials_results_{phasic_name}")
#         )  # preserve dtypes
#         result = (
#             pid.groupby(condition_cols)[pid_value_cols].agg(["mean", "std"]).
#             reset_index()
#         )
#         result.columns = ["{}_{}".format(col[0], col[1]) if col[1] else col[0]
#         for col in result.columns]
#         result.to_feather(os.path.join(dir, f"final_results_{phasic_name}"))
