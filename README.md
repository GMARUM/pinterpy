# pinterpy
Python function for vertical interpolation of WRF (Weather Research and Forecasting Model) output to pressure levels.

Prerequisites:

First of all, a python environment is needed. Conda distribution is highly recommended. The installation of the python libraries os, sys, ast, numpy, netCDF4 and wrf is a prerequisite for the running of interpy. Some of these libraries will probably be installed by default.

Installation and environment checking:

Once the installation is completed, please type 'python' in a terminal, and check that you are able to import these libraries. 

Namelist completion:

After that, fill in the interp-namelist file following the guidelines included in the README.interp-namelist file. 

Execution:

Finally, run the code by typing the following command on the terminal:

$ python interpy.py namelist/interp-namelist 

Note for troubleshooting: If you installed conda and 'python' command is not found in the terminal, you probably need to enter the conda environment by typing 'conda activate' on the terminal. If installation of conda was successful, it should have modified your bashrc file to allow you use conda commands. If not, please find your bashrc file (~/.bashrc on Linux, ~/.bash_profile on Mac OS) and add the following line by using vim, nano, or any editor you may be used to use:

export PATH="PTAB:$PATH"

where PTAB should represent the path to the bin folder of your anaconda installation (e.g., /Users/guest/anaconda3/bin)
