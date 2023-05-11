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

from src.util import spiking_names
from src.util import (
    combine_data,
    hebb_spiking_files,
    anti_spiking_files,
    scal_spiking_files,
)


pid_cols = [
    "k_condition",  # experimental condition (1=control case; 2=pop 1 OFF; 3=pop 2 OFF)
    "pathway",  # pathway (signal group)
    "learning_time",  # learning time (e.g. 0,1,2,5,10,20 mins)
    "mi",
    "u1",
    "u2",
    "u3",
    "r",
    "sy",
    "mi_13",
    "r_13",
    "sy_13",
    "un_13",
    "mi_12",
    "r_12",
    "sy_12",
    "un_12",
    "mi_23",
    "r_23",
    "sy_23",
    "un_23",
]

pid_cols_dict = {
    "4D": spiking_names,
    "in1_excluded": [name for name in spiking_names if "in1" not in name],
    "in2_excluded": [name for name in spiking_names if "in2" not in name],
    "ex_excluded": [name for name in spiking_names if "ex" not in name],
}


def get_pid_cols(cond, phasic=True):
    """returns list of columns for condition"""
    suffix = "_ph"
    if not phasic:
        suffix = "_t"
    return [col + suffix for col in pid_cols_dict[cond]]


def filter_data(data, k, pw, tm):
    """filter data on k, pathway, time"""
    output = data[data["k_condition"] == k]  # select condition k=1,2,3
    output = output[output["pathway"] == pw]  # select pathway pw=1,9
    output = output[output["learning_time"] == tm]  # select time point wt=0,1,2,5,10,20
    return output


#%% Define necessary PID functions using infotheory library


def pid_3D(df, k, pw, t, cond, phasic=True):
    """3-dimensional partial information decomposition (2 inputs, 1 target)"""
    cols = get_pid_cols(cond, phasic)  # get columns
    data = filter_data(df, k, pw, t)[
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


def pid_4D(df, k, pw, t, cond, phasic=True):
    """4-dimensional partial information decomposition (3 inputs, 1 target)"""
    cols = get_pid_cols(cond, phasic)  # get columns
    data = filter_data(df, k, pw, t)[
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


def pid_table(df, phasic=True):
    """creates table of PID values from data"""
    k_values = df["k_condition"].unique().tolist()
    pw_values = df["pathway"].unique().tolist()
    t_values = df["learning_time"].unique().tolist()
    n_rows = len(k_values) * len(pw_values) * len(t_values)
    df_pid = pd.DataFrame(index=range(n_rows), columns=pid_cols)
    row_idx = 0
    for k in k_values:  # for all conditions
        for pw in pw_values:  # loop over pathways
            for t in t_values:  # loop over time points
                mi = u1 = u2 = u3 = r = sy = mi_13 = r_13 = sy_13 = un_13 = 0
                mi_12 = r_12 = sy_12 = un_12 = mi_23 = r_23 = sy_23 = un_23 = 0
                if k == 1:
                    mi, u1, u2, u3, r, sy = pid_4D(df, k, pw, t, "4D", phasic)
                    mi_23, r_23, sy_23, un_23, un_32 = pid_3D(
                        df, k, pw, t, "ex_excluded", phasic
                    )
                if k != 3:
                    mi_13, r_13, sy_13, un_13, un_31 = pid_3D(
                        df, k, pw, t, "in1_excluded", phasic
                    )
                if k != 2:
                    mi_12, r_12, sy_12, un_12, un_21 = pid_3D(
                        df, k, pw, t, "in2_excluded", phasic
                    )
                vals = [
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
    return df


# #%%
# hebb_spiking = combine_data(hebb_spiking_files)
#
#
# #%%
# example = hebb_spiking[hebb_spiking['trials_group']==1]
#
# #%%
#
# """3-dimensional partial information decomposition (2 inputs, 1 target)"""
# cols = get_pid_cols("ex_excluded", True)  # get columns
# data = filter_data(example, 1, 9, 20)[
#     cols
# ].to_numpy()  # filter data and convert to numpy
# dims = np.shape(data)[1]
# it = infotheory.InfoTools(dims, 3)
# it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
# it.add_data(data)
# mi = it.mutual_info([0, 1, 1])
# r = it.redundant_info([0, 1, 2])
# s = it.synergy([0, 1, 2])
# u1 = it.unique_info([0, 1, 2])
# u2 = it.unique_info([0, 2, 1])


# df = PID_table(example)

#%%
# mi, u1, u2, u3, r, sy = pid_4D(example, 1, 9, 20, "4D", True)
#%%

# mi_23, r_23, sy_23, un_23, un_32 = pid_3D(example, 1, 9, 20, "ex_excluded", True)


#%% combine functions above to create full PID table

#
# def hebb_PID_table(data):
#     df = pd.DataFrame(
#         columns=[
#             "subcondition",
#             "pathway",
#             "time",
#             "total_mi",
#             "ex_un",
#             "in1_un",
#             "in2_un",
#             "redundancy",
#             "synergy",
#             "mi_13",
#             "r_13",
#             "sy_13",
#             "un_13",
#             "mi_12",
#             "r_12",
#             "sy_12",
#             "un_12",
#             "mi_23",
#             "r_23",
#             "sy_23",
#             "un_23",
#         ]
#     )  # create empty dataframe
#     k = 1  # just for the top condition i.e. hebbian
#     for pw in [1, 9]:  # loop over pathways
#         for t in [0, 1, 2, 5, 10, 20]:  # loop over time points
#             dat = pid_cols(filter_data(data, k, pw, t)).to_numpy()
#             dat_in1off = pid_p1off_cols(
#                 filter_data(data, k, pw, t)
#             ).to_numpy()  # excluding inhibitory population 1
#             dat_in2off = pid_p2off_cols(
#                 filter_data(data, k, pw, t)
#             ).to_numpy()  # excluding inhibitory population 2
#             dat_exoff = pid_inhib_cols(
#                 filter_data(data, k, pw, t)
#             ).to_numpy()  # excluding excitatory population
#             mi = (
#                 u1
#             ) = (
#                 u2
#             ) = (
#                 u3
#             ) = (
#                 r
#             ) = (
#                 sy
#             ) = (
#                 mi_23
#             ) = (
#                 r_23
#             ) = (
#                 sy_23
#             ) = un_23 = mi_13 = r_13 = sy_13 = un_13 = mi_12 = r_12 = sy_12 =
#             un_12 = 0
#             if k == 1:
#                 mi, u1, u2, u3, r, sy = pid_4D(dat)
#                 mi_23, r_23, sy_23, un_23, un_32 = pid_3D(dat_exoff)
#             if k != 3:
#                 mi_13, r_13, sy_13, un_13, un_31 = pid_3D(dat_in1off)
#             if k != 2:
#                 mi_12, r_12, sy_12, un_12, un_21 = pid_3D(dat_in2off)
#
#             df = df.append(
#                 {
#                     "subcondition": k,
#                     "pathway": pw,
#                     "time": t,
#                     "total_mi": mi,
#                     "ex_un": u1,
#                     "in1_un": u2,
#                     "in2_un": u3,
#                     "redundancy": r,
#                     "synergy": sy,
#                     "mi_13": mi_13,
#                     "r_13": r_13,
#                     "sy_13": sy_13,
#                     "un_13": un_13,
#                     "mi_12": mi_12,
#                     "r_12": r_12,
#                     "sy_12": sy_12,
#                     "un_12": un_12,
#                     "mi_23": mi_23,
#                     "r_23": r_23,
#                     "sy_23": sy_23,
#                     "un_23": un_23,
#                 },
#                 ignore_index=True,
#             )
#     df["time"].replace({2: 2.5}, inplace=True)
#     return df
