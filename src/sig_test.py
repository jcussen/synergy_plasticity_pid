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
    pid_value_cols,
)


def get_feather_data(dir, condition, file_name, phasic_name):
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

    surrogates = get_feather_data(
        surrogates_dir, condition, "trials_surrogate", phasic_name
    )
    results = get_feather_data(results_dir, condition, "final_results", phasic_name)

    # Create an empty dataframe to store the p-values
    p_values_df = pd.DataFrame(columns=pid_value_cols)

    for name, results_group in results.groupby(condition_cols):
        surrogate_group = surrogates.groupby(condition_cols).get_group(name)

        p_values = {}
        for col in pid_value_cols:
            # Check if either group has all the same values
            if len(set(results_group[col])) == 1 or len(set(surrogate_group[col])) == 1:
                p_values[col] = np.nan
            else:
                stat, p = mannwhitneyu(
                    results_group[col], surrogate_group[col], alternative="two-sided"
                )
                p_values[col] = p

        p_values_df = p_values_df.append(p_values, ignore_index=True)
    return p_values_df
