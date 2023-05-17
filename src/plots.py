import matplotlib.pyplot as plt
import os

import pandas as pd

from src.util import figures_dir, results_dir, condition_cols, pid_value_cols, schemes

#%% All dictionaries for names of columns/variables

col_dic = {
    "mi_mean": "$I(X_{1}, X_{2}, X_{3}; T)$",
    "r_mean": "$I_{\partial}^{\{1\} \{2\} \{3\}}$",
    "u1_mean": "$I_{\partial}^{\{1\}}$",
    "sy_mean": "$I_{\partial}^{\{1 2 3\}}$",
    "sy_12_mean": "$I_{\partial}^{\{1 2\}}*$",
    "sy_13_mean": "$I_{\partial}^{\{1 3\}}*$",
}

pref_col_dic_p1off = {
    "mi_13_mean": "$I(X_{1}, X_{3}; T)$",
    "r_13_mean": "$I_{\partial}^{\{1\} \{3\}}$",
    "un_13_mean": "$I_{\partial}^{\{1\}}$",
    "sy_13_mean": "$I_{\partial}^{\{1 3\}}$",
}

nonpref_col_dic_p1off = {
    "mi_13_mean": "$I(Y_{1}, Y_{3}; T)$",
    "r_13_mean": "$I_{\partial}^{\{1\} \{3\}}$",
    "un_13_mean": "$I_{\partial}^{\{1\}}$",
    "sy_13_mean": "$I_{\partial}^{\{1 3\}}$",
}

pref_col_dic_p2off = {
    "mi_12_mean": "$I(X_{1}, X_{2}; T)$",
    "r_12_mean": "$I_{\partial}^{\{1\} \{2\}}$",
    "un_12_mean": "$I_{\partial}^{\{1\}}$",
    "sy_12_mean": "$I_{\partial}^{\{1 2\}}$",
}

nonpref_col_dic_p2off = {
    "mi_12_mean": "$I(Y_{1}, Y_{2}; T)$",
    "r_12_mean": "$I_{\partial}^{\{1\} \{2\}}$",
    "un_12_mean": "$I_{\partial}^{\{1\}}$",
    "sy_12_mean": "$I_{\partial}^{\{1 2\}}$",
}

main_col_dic = {
    1: {1: col_dic, 9: col_dic},  # both populations on
    2: {1: nonpref_col_dic_p1off, 9: pref_col_dic_p1off},  # pop 1 off
    3: {1: nonpref_col_dic_p2off, 9: pref_col_dic_p2off},
}  # pop 2 off

#%%


def plot_err_bar(data, big_col_dict, cond, pw, fold_path):
    fullpath = str(fold_path) + "/ERR_cond_" + str(cond) + "_pw" + str(pw)
    col_dict = big_col_dict.get(cond).get(pw)
    fig, ax = plt.subplots()
    df = data[data["pathway"] == pw]
    df = df[df["k_condition"] == cond]
    cols = list(col_dict.keys())
    colours = [
        "#1f77b4",
        "#d62728",
        "#2ca02c",
        "#ff7f0e",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    for count, i in enumerate(cols):
        std_str = i.replace("mean", "std")
        ax.errorbar(
            x=df["learning_time"],
            y=df[i],
            yerr=df[std_str],
            label=col_dict.get(i),
            color=colours[count],
            ecolor="black",
            capsize=2,
        )
    ax.legend()
    ax.set_ylabel("Bits")
    ax.set_xlabel("Time (mins)")
    plt.savefig(fullpath, bbox_inches="tight")
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
# plot_err_bar(data, main_col_dic, 1, 9, dir)

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
