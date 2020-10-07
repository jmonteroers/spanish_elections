The main purpose of this repo is to provide tools to work with data from
Spanish elections.

Currently, I am only working with results from November 2019
elections extracted from official sources and I am translating serial code that
simply did the job to a more modular solution.

### Data
All data for this project is stored in data folder. The data folder itself
contains two subfolders, input and output.

#### Data in input folder
- Zip folders downloaded from http://www.infoelectoral.mir.es/infoelectoral/min/areaDescarga.html?method=inicio Zip folder only contains
the excel files also presented in data/input

#### Data in output folder
- Will be explained once code is cleaned up


### To-do list
- adapt dhondt.py to new results and general data table structures
  - idea: for simplicity, create function that looks up seats on a dictionary while
  getting voting data in a pandas.DataFrame
- add functionality to support vote translations (e.g. 10 % of
  Cs votes move to PSOE)
    - keep pandas format or translate to new object?
