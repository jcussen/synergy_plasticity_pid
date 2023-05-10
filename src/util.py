"""
This file contains utility functions and variables
for reading and processing neuronal simulation data.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# get file paths and names
working_dir = os.getcwd()
spiking_data_dir = os.path.join(working_dir, "files", "spiking_data")
schemes = ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]
scheme_paths = [os.path.join(spiking_data_dir, scheme) for scheme in schemes]
hebb_spiking_files, anti_spiking_files, scal_spiking_files = [
    [file for file in Path(scheme).glob("**/*") if file.is_file()]
    for scheme in scheme_paths
]

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

# phasic and tonic column names
phasic_cols = [name + "_ph" for name in spiking_names]
tonic_cols = [name + "_t" for name in spiking_names]

# the desired column order for combined data
combined_cols = condition_cols + step_input_cols + phasic_cols + tonic_cols


# data processing functions
def read_data(filepath):
    """reads spiking data from .dat format into dataframe with columns"""
    data = np.loadtxt(filepath)
    df = pd.DataFrame(data=data, columns=spiking_data_cols)
    return df


def combine_data(scheme_filepaths):
    """combines .dat files of spiking data for a plasticity condition"""
    spiking_list = [read_data(filepath) for filepath in scheme_filepaths]
    spiking_df = pd.concat(spiking_list)
    # reorder and drop unnecessary cols
    sorted_df = spiking_df.sort_values(by=condition_cols)
    df = sorted_df[combined_cols]
    return df


# helper functions
def get_n_trials(df):
    """returns total number of trials for each subcondition"""
    unique_conditions = df[condition_cols].drop_duplicates().shape[0]
    n_trials = df.shape[0] / unique_conditions
    return int(n_trials)


#%%
anti_spiking = combine_data(anti_spiking_files)

n_trials = get_n_trials(anti_spiking)

#%%

for filepath in anti_spiking_files:
    print(filepath)

#%%
# anti_test = read_data(
#     "/Users/JoeCussen/Documents/Publications/neuroscience/synergy_plasticity/repos/synergy_plasticity_pid/files/spiking_data/Hebbian_antiHebbian/561825436_50000.dat"
# )
