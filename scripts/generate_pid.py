import os
import sys

#%%
working_dir = "synergy_plasticity_pid"
current_dir = os.getcwd()
os.chdir(current_dir.split(working_dir)[0] + working_dir)
sys.path.append(os.getcwd())
#%%

from src.pid import pid_table, pid_4D
from src.util import (
    combine_data,
    hebb_spiking_files,
    anti_spiking_files,
    scal_spiking_files,
)


#%%
anti_spiking = combine_data(anti_spiking_files)


#%%
example = anti_spiking[anti_spiking["trials_group"] == 1]

#%%
df = pid_table(example)

#%%
print(df)

# mi, u1, u2, u3, r, sy = pid_4D(example, 1, 9, 20, "4D", True)
