"""
This file contains utility functions and variables
for reading and processing neuronal simulation data.
"""

import pandas as pd
import numpy as np
import os

# get file paths and names
working_dir = os.getcwd()
spiking_data_dir = os.path.join(working_dir, "files", "spiking_data")
plasticity_schemes = ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]
hebb_spiking, anti_spiking, scal_spiking = [
    os.path.join(spiking_data_dir, scheme) for scheme in plasticity_schemes
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


# data processing functions
def read_data(filepath):
    """reads spiking data from .dat format into dataframe with columns"""
    data = np.loadtxt(filepath)
    df = pd.DataFrame(data=data, columns=spiking_data_cols)
    return df


#%%
