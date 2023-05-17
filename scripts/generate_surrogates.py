import os
import sys
import pandas as pd
import numpy as np

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.pid import generate_pid_results
from src.util import spiking_files_dict

#%% generate surrogates

seed = 0
for phasic in [True, False]:
    for condition in spiking_files_dict.keys():
        for i in range(10):
            generate_pid_results(
                condition, phasic=phasic, surrogate=True, random_seed=seed
            )
            seed += 1

# %%

# path = '/Users/JoeCussen/Documents/Publications/neuroscience/synergy_plasticity/
# repos/synergy_plasticity_pid/files/surrogates/Hebbian/trials_results_phasic'
# surr_example = pd.read_feather(path)
