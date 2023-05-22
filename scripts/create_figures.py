"""
This script creates the visualisations of results used in this
research paper.
Run this script third.
"""

import os
import sys

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

#%% generate figures
