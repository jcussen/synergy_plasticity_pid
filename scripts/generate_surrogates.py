"""
This script creates surrogate PID values based on shuffled data,
which is used to test the statistical significance of results.
Run this script second.
"""

import os
import sys

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
        generate_pid_results(
            condition, phasic=phasic, surrogate=True, seed=seed, n_surrogates=10
        )
        seed += 1
