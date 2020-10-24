## Introduction
The purpose of this package is to provide tools to run counterfactual simulations of the Spanish elections and analyse the results. Additionally, it will make some election-related data easily accessible.

The current version is an unstable version. In fact, I am only working with results from November 2019 General Elections extracted from [official sources](http://www.infoelectoral.mir.es/infoelectoral/min/areaDescarga.html?method=inicio) and I am translating serial code that simply did the job to a more modular solution with a package structure.

## Installation
First, get the source. Then, within your shell, move to the root directory of your local installation, and run:
```
python3 -m pip install .
```

An alternative is to run the `install_with_venv.sh` bash script (only works in Unix systems). This script will create a virtual environment, install this package and its dependencies, and add the virtual environment as a kernel to your jupyter notebook installation (it's what I use myself to get the package running in my jupyter notebook). You can also pass a number of arguments to this script. For more info, check the file.

### Plans for the future
Some functions will be added to transform the original votes. For example, to transfer votes from one political party to another (already available at the national level) or to extrapolate the result of a survey at the national level to provincial level data, and thus obtain the final results of the elections. Similarly, it will be interesting to add functions to work with confidence intervals at the survey level.

Finally, it would be nice to add some functions to represent the results in a graphical and interactive manner, e.g. using plotly maps.


### To-do list
- finish introductory jupyter notebook
  - add simulation
  - add vote transfers at national level
- add data to package
- add functions to transform survey results at different levels (national, provincial) to elections outcome
- add ballot transfers at local level(interesting?)
- add data from different elections
- add interactive maps for results
