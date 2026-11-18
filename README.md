# Multi-objective travelling salesman problem

This is the code for my Masters project. It looks at the travelling salesman problem with more than one objective, where every edge between two cities has several weights (distance and time, for example) and a tour is scored on each of them separately. There is usually no single best tour, so the aim is to find the Pareto front: the set of tours that no other tour beats on every objective at once.

The front is searched for with NSGA-II, and a large part of the project is about visualising how a population moves over a run. With three or more objectives the population cannot be plotted directly, so the objective vectors are reduced to two dimensions (mostly with PCA, with MDS and t-SNE also tried) and plotted against the generation number in 3D. The write-up is in `FINAL report.pdf`, and the presentation slides are in `submission/`.

## How it works

Problems are random and fully connected. Each pair of cities gets one random integer weight per objective, and city 0 is the fixed start, so a solution is a permutation of the other cities.

Each generation of NSGA-II goes roughly like this:

1. The population is split into fronts by non-dominated sorting.
2. A mating pool is filled a whole front at a time. The front that does not fit is cut down by crowding distance, which favours solutions in less crowded parts of the front.
3. Children are made with a block crossover (a block of one parent is kept in place and the rest comes from the other parent) and a mutation that swaps two cities.
4. Parents and children are pooled and the best fronts are kept for the next generation, so good solutions are never lost.

For the plots, the objective vectors from every generation of a run are collected and a PCA is fitted on all of them together, so each generation is drawn on the same two axes. Points are coloured by which objective is largest for that solution.

## Layout

- `submissionCode/` is the version that was handed in. `main.py` runs NSGA-II on a random 30 city, 3 objective problem and opens an interactive Plotly plot of the run. `ECMM428notebook.ipynb` is the notebook used for the demonstration. `submission/submissionCode/` is a deliberate copy, as its README says.
- `code/MTSP/` is the development code. The top level is a plain single objective genetic algorithm that came first. `Multi-Obj/2D NSGA-II` is NSGA-II for two objectives with a hypervolume measure, and `Multi-Obj/ND NSGA-II` is the version that works for any number of objectives.
- `code/MTSP/Multi-Obj/ND NSGA-II/tests.py` (and the three `testsCopy` files, which each do one objective count) runs 3, 4 and 5 objective problems with 20 to 32 cities and logs every generation to a text file. `dfConversion/` turns those logs into PCA dataframes and `dfToGraph/` saves images of them from four camera angles.
- `code/MTSP/Multi-Obj/visualisation/` holds earlier plotting experiments: a single generation and its front (`singleGenVis`), whole runs in matplotlib and Plotly (`multiGenVis`), and MDS on the objectives (`withMDS`). It has its own copy of the two objective NSGA-II code.
- `code/MTSP/Multi-Obj/mdsTesting/`, `pymooTesting/` and `code/plottingTests/` are small tests of MDS, pymoo and Plotly.
- `code/dimension reduction/` compares PCA and t-SNE on a saved run.
- `code/GRAPHS/` and `code/2-D images/` run NSGA-II and save the images of the results. `lib.py` in each holds the solution and population code in a single file.
- `code/MTSP/Multi-Obj/LMDS-master/` is a third party landmark MDS implementation and is not my code.

## Running it

The code needs Python 3.9 or later and the packages in `requirements.txt`:

```
pip install -r requirements.txt
```

`kaleido` is only needed by the scripts that save Plotly figures as images. The notebook also needs Jupyter.

The scripts import their neighbours by name and read or write files in the current folder, so run each one from its own folder. For the submitted version:

```
cd submissionCode
python3 main.py
```

The problem size, number of generations, population size, mutation rate and truncation rate are set at the top of `main.py`. Larger problems and populations take a while, since the non-dominated sorting compares every pair of solutions.
