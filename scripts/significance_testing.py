import os
import sys
import pandas as pd

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.util import spiking_files_dict

#%%

# get all paths

# combine data

# check Gaussianity

# calc mean and standard deviation