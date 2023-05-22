import os
import sys
import re

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt


working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())


#%%


# sig_df = generate_p_values()

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
