"""
This script creates the visualisations of results used in this
research paper.
Run this script third.
"""

import os
import sys
import pandas as pd

working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.sig_test import get_norm_sig
from src.plots import plot_pid, plot_sig
from src.util import figures_dir

#%% test significance and get normalised data
df = get_norm_sig()

#%% generate figures

plot_sig(df, 1, 9, os.path.join(figures_dir, "Hebbian"), p_value=0.05)
