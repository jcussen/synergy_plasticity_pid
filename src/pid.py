import pandas as pd
import numpy as np
import infotheory
import os
import sys

# set up working directory
working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())

from src.util import (
    pid_cols,
    pid_cols_dict,
    spiking_files_dict,
    condition_cols,
    pid_value_cols,
    results_dir,
    surrogates_dir,
    combine_data,
    shuffle_data,
    filter_data,
)


def get_pid_cols(cond, phasic=True):
    """returns list of columns for condition"""
    suffix = "_ph"
    if not phasic:
        suffix = "_t"
    return [col + suffix for col in pid_cols_dict[cond]]


#%% Define necessary PID functions using infotheory library


def pid_3d(df, g, k, pw, t, cond, phasic=True):
    """3-dimensional partial information decomposition (2 inputs, 1 target)"""
    cols = get_pid_cols(cond, phasic)  # get columns
    data = filter_data(df, k, pw, t, g)[
        cols
    ].to_numpy()  # filter data and convert to numpy
    # set up infotheory object
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # get PID terms
    mi = it.mutual_info([0, 1, 1])
    r = it.redundant_info([0, 1, 2])
    s = it.synergy([0, 1, 2])
    u1 = it.unique_info([0, 1, 2])
    u2 = it.unique_info([0, 2, 1])
    rnd = lambda x: np.round(x, decimals=4)
    return rnd(mi), rnd(r), rnd(s), rnd(u1), rnd(u2)


def pid_4d(df, g, k, pw, t, cond, phasic=True):
    """4-dimensional partial information decomposition (3 inputs, 1 target)"""
    cols = get_pid_cols(cond, phasic)  # get columns
    data = filter_data(df, k, pw, t, g)[
        cols
    ].to_numpy()  # filter data and convert to numpy
    # set up infotheory object
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # get PID terms
    mi = it.mutual_info([0, 1, 1, 1])
    u1 = it.unique_info([0, 1, 2, 3])
    u2 = it.unique_info([0, 2, 1, 3])
    u3 = it.unique_info([0, 2, 3, 1])  # the unique variable is where the 1 is!!!!
    r = it.redundant_info([0, 1, 2, 3])
    s = it.synergy([0, 1, 2, 3])
    rnd = lambda x: np.round(x, decimals=4)
    return rnd(mi), rnd(u1), rnd(u2), rnd(u3), rnd(r), rnd(s)


#%% combine functions above to create full PID table


def pid_analysis(df, phasic=True):
    """creates table of PID values from data"""
    g_values = df["trials_group"].unique().tolist()
    k_values = df["k_condition"].unique().tolist()
    pw_values = df["pathway"].unique().tolist()
    t_values = df["learning_time"].unique().tolist()
    n_rows = len(g_values) * len(k_values) * len(pw_values) * len(t_values)
    df_pid = pd.DataFrame(index=range(n_rows), columns=pid_cols)
    row_idx = 0
    for g in g_values:  # for all trial groups
        print("Calculating PID for trials group " + str(g))
        for k in k_values:  # for all conditions
            for pw in pw_values:  # loop over pathways
                for t in t_values:  # loop over time points
                    mi = u1 = u2 = u3 = r = sy = mi_13 = r_13 = sy_13 = un_13 = 0
                    mi_12 = r_12 = sy_12 = un_12 = mi_23 = r_23 = sy_23 = un_23 = 0
                    if k == 1:
                        mi, u1, u2, u3, r, sy = pid_4d(df, g, k, pw, t, "4D", phasic)
                        mi_23, r_23, sy_23, un_23, un_32 = pid_3d(
                            df, g, k, pw, t, "ex_excluded", phasic
                        )
                    if k != 3:
                        mi_13, r_13, sy_13, un_13, un_31 = pid_3d(
                            df, g, k, pw, t, "in1_excluded", phasic
                        )
                    if k != 2:
                        mi_12, r_12, sy_12, un_12, un_21 = pid_3d(
                            df, g, k, pw, t, "in2_excluded", phasic
                        )
                    vals = [
                        g,
                        k,
                        pw,
                        t,
                        mi,
                        u1,
                        u2,
                        u3,
                        r,
                        sy,
                        mi_13,
                        r_13,
                        sy_13,
                        un_13,
                        mi_12,
                        r_12,
                        sy_12,
                        un_12,
                        mi_23,
                        r_23,
                        sy_23,
                        un_23,
                    ]
                    row_vals = {name: val for name, val in zip(pid_cols, vals)}
                    df_pid.loc[row_idx] = row_vals
                    row_idx += 1
    return df_pid


def generate_pid_results(
    condition="Hebbian", phasic=True, surrogate=False, seed=0, n_surrogates=1
):
    """generates final PID results from spiking data"""
    if condition not in ["Hebbian", "Hebbian_antiHebbian", "Hebbian_scaling"]:
        raise ValueError(
            "Invalid condition provided: must be 'Hebbian', 'Hebbian_antiHebbian' "
            "or 'Hebbian_scaling'"
        )
    phasic_name = "phasic"
    if not phasic:
        phasic_name = "tonic"

    results = "results"
    dir = os.path.join(results_dir, condition)
    if surrogate:
        results = f"surrogate_{str(seed)}"
        dir = os.path.join(surrogates_dir, condition)

    # check if exists already:
    if os.path.isfile(os.path.join(dir, f"trials_{results}_{phasic_name}")):
        print(f"{results} data already exists for {phasic_name} {condition} condition")
        return
    if not os.path.exists(dir):
        os.makedirs(dir)

    spiking_files = spiking_files_dict[condition]
    print(f"Processing data ({condition})")
    spiking = combine_data(spiking_files)

    if surrogate:
        pid_dfs = []
        random_seed = seed * n_surrogates
        for i in range(n_surrogates):
            print(f"Surrogate dataset {random_seed}")
            print(f"Shuffling data ({condition})")
            shuffled_spiking = shuffle_data(spiking, phasic, random_seed)

            print(f"Generating PIDs ({condition})")
            pid = pid_analysis(shuffled_spiking, phasic)
            pid["random_seed"] = random_seed
            pid_dfs.append(pid)

            random_seed += 1

        print(f"Saving results ({condition})")
        surrogate_pids = pd.concat(pid_dfs).reset_index(drop=True)
        surrogate_pids.to_feather(os.path.join(dir, f"trials_{results}_{phasic_name}"))
    else:
        print(f"Generating PIDs ({condition})")
        pid = pid_analysis(spiking, phasic)
        pid.to_feather(os.path.join(dir, f"trials_{results}_{phasic_name}"))
        pid = pd.read_feather(
            os.path.join(dir, f"trials_results_{phasic_name}")
        )  # preserve dtypes
        result = (
            pid.groupby(condition_cols)[pid_value_cols]
            .agg(["mean", "std"])
            .reset_index()
        )
        result.columns = [
            "{}_{}".format(col[0], col[1]) if col[1] else col[0]
            for col in result.columns
        ]
        result.to_feather(os.path.join(dir, f"final_results_{phasic_name}"))
