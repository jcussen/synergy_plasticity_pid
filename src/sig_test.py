"""
This file contains functions for significance testing of neuronal data,
comparing it to the results for surrogate data.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import mannwhitneyu

from src.util import (
    surrogates_dir,
    results_dir,
    condition_cols,
    plot_pid_cols,
    pid_value_cols,
    phasic_names,
)


def get_feather_data(dir, condition, file_name, phasic_name):
    """gets data from a directory"""
    condition_dir = os.path.join(dir, condition)
    filepaths = [
        file
        for file in Path(condition_dir).iterdir()
        if file.is_file() and file_name in file.name and phasic_name in file.name
    ]
    if filepaths == []:
        print(
            f"{file_name} data does not exist for {phasic_name} {condition} condition"
        )
        return
    elif len(filepaths) > 1:
        print(f"Multiple files for {file_name} {phasic_name} {condition} condition")
        return
    else:
        filepath = filepaths[0]
    return pd.read_feather(filepath)


def add_noise(df_in, col):
    """Adds small amount of noise to homogeneous data"""
    df = df_in.copy()
    noise = np.random.normal(0, 0.0001, size=df[col].shape)
    df[col] = df[col] + noise
    df.loc[df[col] < 0, col] = 0  # set all negative values to zero
    return df[col]


def generate_p_values(condition="Hebbian", phasic=True):
    """compares surrogate and results data using statistical test"""
    # set up
    if condition not in ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]:
        raise ValueError(
            "Invalid condition provided: must be 'Hebbian', 'Hebbian_antiHebbian' "
            "or 'Hebbian_scaling'"
        )
    phasic_name = phasic_names[phasic]

    # get surrogate data
    surrogates = get_feather_data(
        surrogates_dir, condition, "trials_surrogate", phasic_name
    )
    results = get_feather_data(results_dir, condition, "trials_results", phasic_name)

    # Create an empty dataframe to store the p-values
    p_values_df = pd.DataFrame(columns=plot_pid_cols)

    for name, results_group in results.groupby(condition_cols):
        surrogate_group = surrogates.groupby(condition_cols).get_group(name)

        p_values = {}
        for col in plot_pid_cols:
            # Check if either group has all the same values
            if col in condition_cols:
                p_values[col] = results_group.reset_index(drop=True).loc[0, col]
            else:
                res_group = results_group[col]
                surr_group = surrogate_group[col]
                if len(set(results_group[col])) == 1:
                    res_group = add_noise(results_group, col)
                if len(set(surrogate_group[col])) == 1:
                    surr_group = add_noise(surrogate_group, col)
                stat, p = mannwhitneyu(res_group, surr_group, alternative="two-sided")
                p_values[col] = p

        p_values_df = p_values_df.append(p_values, ignore_index=True)
    return p_values_df


def normalise_results(df_results):
    """normalises the PID results with respect to mutual information"""
    df_norm = df_results.copy()
    norm_cols = [col + "_mean" for col in pid_value_cols]
    df_norm[norm_cols] = df_norm[norm_cols].div(df_norm["mi_mean"], axis=0)
    return df_norm


def get_norm_sig(condition="Hebbian", phasic=True):
    """creates combined dataframe of normalised results and p values for plotting"""
    # set up
    if condition not in ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]:
        raise ValueError(
            "Invalid condition provided: must be 'Hebbian', 'Hebbian_antiHebbian' "
            "or 'Hebbian_scaling'"
        )
    phasic_name = phasic_names[phasic]

    p_values_df = generate_p_values(condition=condition, phasic=phasic)
    p_values_df.rename(
        columns={col: col + "_p" for col in pid_value_cols}, inplace=True
    )

    agg_results = get_feather_data(results_dir, condition, "final_results", phasic_name)
    norm_results = normalise_results(agg_results)

    # combine mean values with p values
    mean_results = norm_results.loc[:, ~norm_results.columns.str.contains("_std")]
    combined_df = mean_results.merge(
        p_values_df, how="left", on=condition_cols, suffixes=("", "_p")
    )

    return combined_df
