# pinterpy
Python function for vertical interpolation of WRF (Weather Research and Forecasting Model) output to pressure levels.

Execution:

First of all, a python environment is needed. Conda distribution is highly recommended. The installation of the python libraries os, sys, ast, numpy, netCDF4 and wrf is a prerequisite for the running of interpy. Some of these libraries will probably be installed by default.

Once the installation is completed, please type 'python' in a terminal, and check that you are able to import these libraries. After that, complete the interp-namelist following the guidelines included in the README.interp-namelist file. Finally, the execution will be available by typing the following on the terminal:

$ python interpy.py namelist/interp-namelist 
