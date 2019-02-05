# pinterpy
Python function for vertical interpolation of WRF (Weather Research and Forecasting Model) output to pressure levels.

### Getting Started

Get a copy of the .py file on the code folder of this project. Follow the steps described below to run it.

### Prerequisites

#### Environment and python distribution

First of all, a python environment is needed. Conda distribution is highly recommended. The installation of the python libraries os, sys, ast, numpy, netCDF4 and wrf is a prerequisite for the running of interpy. Some of these libraries will probably be installed by default.

#### Installation of python required libraries and environment checking

Once the installation is completed, type 'python' in a terminal, and check that you are able to import these libraries. 

### Namelist completion

Fill in the interp-namelist file following the guidelines included in the README.interp-namelist file. 

### Execution:

Finally, run the code by typing the following command on the terminal:

$ python interpy.py namelist/interp-namelist 

#### Note for troubleshooting
If you installed conda and 'python' command is not found in the terminal, you probably need to enter the conda environment by typing 'conda activate' on the terminal. If installation of conda was successful, it should have modified your bashrc file to allow you use conda commands. If not, please find your bashrc file (~/.bashrc on Linux, ~/.bash_profile on Mac OS) and add the following line by using vim, nano, or any editor you may be used to use:

export PATH="PTAB:$PATH"

where PTAB should represent the path to the bin folder of your anaconda installation (e.g., /Users/guest/anaconda3/bin)

### Built With
* [Anaconda distribution](https://www.anaconda.com/distribution/) - The World's Most Popular Python/R Data Science Platform
* [Anaconda-navigator](https://anaconda.org/anaconda/anaconda-navigator) - Desktop graphical user interface
* [Spyder IDE](https://www.spyder-ide.org) - The Scientific Python Development Environment
* [Python 3.7.0]
* [NCAR wrf-python](https://rometools.github.io/rome/) - Used to perform the vertical interpolation
* Other used python libraries: os, sys, ast, numpy, netCDF4.

### Contributing

Please visit our research group website (www.um.es/gmar) and fill the contact form at the end for contributing or if you wish to receive further details on our code.

### Version

A single version of this function will be available, and it should exhibit system-independence. 

### Authors

* **Enrique Pravia Sarabia** - 
[eps22](https://github.com/eps22)
[Enrique Pravia-Sarabia](https://es.linkedin.com/in/enrique-pravia-sarabia)

Meet the GMAR complete team at www.um.es/gmar.

### License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

See the [LICENSE](LICENSE) file for details.

### Acknowledgments

* NCAR python library wrf-python (https://github.com/NCAR/wrf-python)
