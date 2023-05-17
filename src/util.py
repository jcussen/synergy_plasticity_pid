"""
This file contains utility functions and variables
for reading and processing neuronal simulation data.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# set up working directory
working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

# get file paths and names
working_dir = os.getcwd()
spiking_data_dir = os.path.join(working_dir, "files", "spiking_data")
results_dir = os.path.join(working_dir, "files", "results")
surrogates_dir = os.path.join(working_dir, "files", "surrogates")
figures_dir = os.path.join(working_dir, "files", "figures")
schemes = ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]
scheme_paths = [os.path.join(spiking_data_dir, scheme) for scheme in schemes]
hebb_spiking_files, anti_spiking_files, scal_spiking_files = [
    [file for file in Path(scheme).glob("**/*") if file.is_file()]
    for scheme in scheme_paths
]

# dictionary for spiking files
spiking_files_dict = {
    "Hebbian": hebb_spiking_files,
    "Hebbian_antiHebbian": anti_spiking_files,
    "Hebbian_scaling": scal_spiking_files,
}

# list of columns and descriptions
spiking_data_cols = [
    "row_num",  # row count
    "k_condition",  # experimental condition (1=control case; 2=pop 1 OFF; 3=pop 2 OFF)
    "learning_time",  # learning time (e.g. 0,1,2,5,10,20 mins)
    "pathway",  # pathway (signal group)
    "step_input",  # step input frequency/firing rate
    "postsynaptic_ph",  # phasic postsynaptic spike count
    "ex_all_ph",  # excitatory population total spike count (phasic)
    "in1_all_ph",  # inhibitory population 1 total spike count (phasic)
    "in2_all_ph",  # inhibitory population 2 total spike count (phasic)
    "ex_pathway_ph",  # excitatory pop. pathway spike count (phasic)
    "in1_pathway_ph",  # inhibitory pop. 1 pathway spike count (phasic)
    "in2_pathway_ph",  # inhibitory pop. 2 pathway spike count (phasic)
    "postsynaptic_t",  # tonic postsynaptic spike count
    "ex_all_t",  # excitatory population total spike count (tonic)
    "in1_all_t",  # inhibitory population 1 total spike count (tonic)
    "in2_all_t",  # inhibitory population 2 total spike count (tonic)
    "ex_pathway_t",  # excitatory pop. pathway spike count (tonic)
    "in1_pathway_t",  # inhibitory pop. 1 pathway spike count (tonic)
    "in2_pathway_t",  # inhibitory pop. 2 pathway spike count (tonic)
]

trials_group_cols = ["trials_group"]  # the label for the set of 10,000 trials

# the columns that define each experimental condition
condition_cols = [
    "k_condition",  # experimental condition (1=control case; 2=pop 1 OFF; 3=pop 2 OFF)
    "pathway",  # pathway (signal group)
    "learning_time",  # learning time (e.g. 0,1,2,5,10,20 mins)
]

# step input columns
step_input_cols = [
    "step_input",  # step input frequency/firing rate
]

# spiking names (pathway only)
spiking_names = [
    "postsynaptic",  # postsynaptic spike count
    "ex_pathway",  # excitatory pop. pathway spike count
    "in1_pathway",  # inhibitory pop. 1 pathway spike count
    "in2_pathway",  # inhibitory pop. 2 pathway spike count
]

# pid condition cols
pid_value_cols = [
    "mi",
    "u1",
    "u2",
    "u3",
    "r",
    "sy",
    "mi_13",
    "r_13",
    "sy_13",
    "un_13",
    "mi_12",
    "r_12",
    "sy_12",
    "un_12",
    "mi_23",
    "r_23",
    "sy_23",
    "un_23",
]

# phasic and tonic column names
phasic_cols = [name + "_ph" for name in spiking_names]
tonic_cols = [name + "_t" for name in spiking_names]

# phasic and tonic column names
phasic_input_cols = [
    name + "_ph" for name in spiking_names if "postsynaptic" not in name
]
tonic_input_cols = [name + "_t" for name in spiking_names if "postsynaptic" not in name]

# pid table columns
pid_cols = trials_group_cols + condition_cols + pid_value_cols

# full condition cols
full_condition_cols = trials_group_cols + condition_cols

# pid analysis dictionary
pid_cols_dict = {
    "4D": spiking_names,
    "in1_excluded": [name for name in spiking_names if "in1" not in name],
    "in2_excluded": [name for name in spiking_names if "in2" not in name],
    "ex_excluded": [name for name in spiking_names if "ex" not in name],
}


# the desired column order for combined data
combined_cols = (
    trials_group_cols + condition_cols + step_input_cols + phasic_cols + tonic_cols
)


# helper functions
def get_n_trials(df):
    """returns total number of trials for each subcondition"""
    unique_conditions = df[condition_cols].drop_duplicates().shape[0]
    n_trials = df.shape[0] / unique_conditions
    return int(n_trials)


# data processing functions
def read_data(filepath):
    """reads spiking data from .dat format into dataframe with columns"""
    data = np.loadtxt(filepath)
    df = pd.DataFrame(data=data, columns=spiking_data_cols)
    return df


def combine_data(scheme_filepaths, trials_per_group=10000):
    """combines .dat files of spiking data for a plasticity condition"""
    spiking_list = [read_data(filepath) for filepath in scheme_filepaths]
    spiking_df = pd.concat(spiking_list)
    # reorder and drop unnecessary cols
    sorted_df = spiking_df.sort_values(by=condition_cols)
    # add label to each trials group
    sorted_df.loc[:, "trials_group"] = (
        sorted_df.groupby(condition_cols).cumcount() // trials_per_group
    ) + 1
    df = sorted_df[combined_cols].reset_index(drop=True)
    return df


def shuffle_data(df, phasic=True, random_seed=0):
    """shuffles data to create surrogate data set"""
    shuffle_cols = phasic_input_cols
    if not phasic:
        shuffle_cols = tonic_input_cols
    np.random.seed(random_seed)  # Set the random seed
    shuffled_df = df.copy()
    shuffled_df[shuffle_cols] = shuffled_df.groupby(full_condition_cols)[
        shuffle_cols
    ].transform(lambda x: np.random.permutation(x))
    return shuffled_df
