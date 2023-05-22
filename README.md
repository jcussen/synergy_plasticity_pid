# Synergy plasticity PID
This repo houses code for the Partial Information Decomposition (PID) analysis of a simulated neuronal plasticity model.


## How to use

1) Run 'learning' and 'step_input' simulations from [this repo](https://github.com/jcussen/synergy_plasticity_simulation) to generate spiking data.
2) Create a new folder from the working directory of this repo called 'files', and copy in the 'spiking_data' folder from the simulation repo so that the path to the data is: `synergy_plasticity_pid/files/spiking_data`.
3) Run `synergy_plasticity_pid/scripts/generate_pid.py` to perform PID analysis.
4) Run `synergy_plasticity_pid/scripts/generate_surrogates.py` to get surrogate dataset which is used to test significance (takes a long time to run).
5) Run `synergy_plasticity_pid/scripts/create_figures.py` to get the results figures used in the paper.
