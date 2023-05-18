import os
import sys
import re
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.stats import mannwhitneyu

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.util import (
    surrogates_dir,
    results_dir,
    condition_cols,
    pid_value_cols,
    filter_data,
    pid_cols,
)

#%%


def get_data(dir, condition, file_name, phasic_name):
    """gets data from a directory"""
    condition_dir = os.path.join(dir, condition)
    filepaths = [
        file
        for file in Path(condition_dir).iterdir()
        if file.is_file() and phasic_name in file.name and phasic_name in file.name
    ]
    if filepaths == []:
        print(
            f"{file_name} data does not exist for {phasic_name} {condition} condition"
        )
        return
    else:
        filepath = filepaths[0]
    return pd.read_feather(filepath)


def generate_p_values(condition="Hebbian", phasic=True):
    """compares surrogate and results data using statistical test"""
    # set up
    if condition not in ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]:
        raise ValueError(
            "Invalid condition provided: must be 'Hebbian', 'Hebbian_antiHebbian' "
            "or 'Hebbian_scaling'"
        )
    phasic_name = "phasic"
    if not phasic:
        phasic_name = "tonic"
    # get surrogate data

    surrogates = get_data(surrogates_dir, condition, "trials_surrogate", phasic_name)
    results = get_data(results_dir, condition, "final_results", phasic_name)

    # Create an empty dataframe to store the p-values
    p_values_df = pd.DataFrame(columns=pid_cols)

    for name, results_group in results.groupby(condition_cols):
        surrogate_group = surrogates.groupby(condition_cols).get_group(name)

        p_values = {}
        for col in pid_cols:
            # Perform Mann-Whitney U test
            stat, p = mannwhitneyu(
                results_group[col], surrogate_group[col], alternative="two-sided"
            )
            p_values[col] = p

        p_values_df = p_values_df.append(p_values, ignore_index=True)


# def process_surrogates(condition = 'Hebbian', phasic = True):
#     '''combines surrogate data and calculates aggregate values'''
#     # set up
#     if condition not in ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]:
#         raise ValueError(
#             "Invalid condition provided: must be 'Hebbian', 'Hebbian_antiHebbian' "
#             "or 'Hebbian_scaling'"
#         )
#     phasic_name = "phasic"
#     if not phasic:
#         phasic_name = "tonic"
#     dir = os.path.join(surrogates_dir, condition)
#     # get filepaths
#     filepaths = [file for file in Path(dir).iterdir() if
#              file.is_file() and 'trials_surrogate'
#              in file.name and phasic_name in file.name]
#     surrogate_dfs = []
#     # read in files and concat
#     for file in filepaths:
#         df = pd.read_feather(file)
#         df['shuffle_seed'] = int(re.findall(r'\d+', file.stem)[0])
#         surrogate_dfs.append(df)
#     surrogates = pd.concat(surrogate_dfs, ignore_index=True)
#     # get mean and standard deviations
#     agg_surrogates = (
#         surrogates.groupby(condition_cols)[pid_value_cols]
#             .agg(["mean", "std"])
#             .reset_index()
#     )
#     agg_surrogates.columns = [
#         "{}_{}".format(col[0], col[1]) if col[1] else col[0]
#         for col in agg_surrogates.columns
#     ]
#     return agg_surrogates
#
# df= process_surrogates()

#%%
# k_values = df["k_condition"].unique().tolist()
# pw_values = df["pathway"].unique().tolist()
# t_values = df["learning_time"].unique().tolist()
# for k in k_values:  # for all conditions
#     for pw in pw_values:  # loop over pathways
#         for t in t_values:  # loop over time points
#             if pw == 9:
#                 df_filt = filter_data(df, k, pw, t)
#                 df_norm = df_filt.copy()
#                 norm_cols = [col for col in pid_value_cols if col!= 'mi']
#                 df_norm[norm_cols]=df_norm[norm_cols].div(df['mi'], axis=0)
#
#                 col = 'sy'
#                 plt.hist(df_norm[col], bins = 'auto')
#                 w, p = stats.shapiro(df_norm[col])
#                 n = len(df_norm[col].to_list())
#                 plt.title(f"k: {k}, pathway: {pw}, time: {t}, n: {n}. p-value: {p}")
#                 plt.show()


# check Gaussianity
# calc mean and standard deviation
