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

from src.sig_test import get_norm_sig, get_feather_data
from src.plots import plot_pid, plot_sig
from src.util import results_dir, figures_dir, spiking_files_dict, phasic_names

#%% generate figures

for phasic in [True, False]:
    for condition in spiking_files_dict.keys():
        df_results = get_feather_data(
            results_dir, condition, "final_results", phasic_names[phasic]
        )
        df_sig = get_norm_sig(condition=condition, phasic=phasic)
        k_values = df_results["k_condition"].unique().tolist()
        pw_values = df_results["pathway"].unique().tolist()
        for k in k_values:  # for all conditions
            for pw in pw_values:  # loop over pathways
                plot_pid(
                    df_results,
                    k,
                    pw,
                    os.path.join(figures_dir, condition),
                    phasic=phasic,
                    condition=condition,
                )
                plot_sig(
                    df_sig,
                    k,
                    pw,
                    os.path.join(figures_dir, condition),
                    p_value=0.05,
                    phasic=phasic,
                    condition=condition,
                )
