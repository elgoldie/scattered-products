# Scattered Products

## Problem Visualization

### Webapp

A webapp developed by Tobit Glenhaber to visualize the problem. Can be accessed either at [this website](https://web.mit.edu/tglenhab/www/scatteredProds.html), or through running webapp/index.html.

### graph.py

A graph tool generated by Eva Goldie with assistance from Holden Watson. Shows the logs of the products generated from pure fillings of 1/2 (blue), 1/3 (orange) and 1/5 (green) for N=1,...,1000. Run in Python 3.7.4.

### optimality.py

A tool created by Eva Goldie with influence from Haley Samuelsen. Finds the optimal pure filling (chosen from 1/2, 1/3, 1/5 and 1/7) for N=1,...,189. 

## Linear Programming

A linear programming tool created by Eva Goldie. Finds the approximately optimal solution for the scattered products problem. Change lp.options.SOLVER (line 72) to 3 for IPOPT, or to 1 for APOPT, allowing Mixed Integer Linear Programming.

