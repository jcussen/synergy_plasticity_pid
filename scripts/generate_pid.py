"""
This script performs PID analysis using the spiking data.
It saves the results to files/results.
Run this script first.
"""

import os
import sys

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.pid import generate_pid_results
from src.util import spiking_files_dict

#%% generate all results

for phasic in [True, False]:
    for condition in spiking_files_dict.keys():
        generate_pid_results(condition, phasic=phasic)
