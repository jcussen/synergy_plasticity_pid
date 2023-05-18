import os
import sys
import re
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

from pathlib import Path

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.util import surrogates_dir, results_dir

#%% Read in data


#%% Clean up file (replace 2 mins with 2.5 mins
surrogate_filepaths = [
    file for file in Path(surrogates_dir).glob("**/*") if file.is_file()
]
results_filepaths = [file for file in Path(results_dir).glob("**/*") if file.is_file()]
all_data_filepaths = surrogate_filepaths + results_filepaths

#%%

# for filepath in all_data_filepaths:
#     df = pd.read_feather(filepath)
#     df['learning_time'] = df['learning_time'].replace(None, 2.5)
#     df.to_feather(filepath)

#%%

df = pd.read_feather(results_filepaths[0])
