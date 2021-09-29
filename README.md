## Introduction

Dependency-free Python package that makes Spanish election data accessible and provides tools to analyse the data and run counterfactual simulations.

The package is under refactoring, removing dependencies, and simplifying its structure. The following functionality is still not available:
- blocs
- examples


Data is extracted from XML files provided by El País website ([an example,
my home city results in 2019!](http://rsl00.epimg.net/elecciones/2019/generales/senado/01/14.xml2)).
To see more details, visit the scrape folder.

## Installation
As any other Python package, cd into root directory and run,
```
python3 -m pip install .
```

This will make the `spanish_elections` available in Python.

### Future Plans

This project is just starting! Here is a to-do list for this package:
- [ ] clean bloc functionality
- [ ] adapt jupyter notebooks to latest changes
  - [ ] add simulation
  - [ ] add vote transfers
- [ ] export results in tabular form as CSV (nice for Data Scientists!)
- [ ] provide survey data
  - [ ] confidence intervals based on survey data
- [ ] extend tools to autonomous communities/provinces/senado
- [ ] add interactive plots with results
  - [ ] map plots
  - [ ] evolution of results

PRs are welcome :)
