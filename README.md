# **ACIT 4610 – Mid-Term Portfolio Project 2**
## Multi-Objective Capacitated Vehicle Routing Problem (MOVRP) Using MOEAs
### Group 3
This repository addresses the **Multi-Objective Capacitated Vehicle Routing Problem (MOVRP)** using **Multi-Objective Evolutionary Algorithms (MOEAs)**. Building on the classical VRP solved in Project 1, this version solves multi-objective VRP instances from CVRPLIB using two evolutionary algorithms: NSGA-II and SPEA2.

Each solution is evaluated on two objectives:
1.  **Total distance traveled**(minimize)
2. **Route imbalance** (Standard deviation of route distances, minimize)
The notebook compares the two algorithms on small, medium, and large VRP instances, using multiple parameter sets and repeated runs.


### Changes from Assignment 1
* Added second objective (route balance).
* Implemented full **NSGA-II** (fast non-dominated sort + crowding distance).
* Implemented **SPEA2** (strength Pareto archive + density measure).
* Added metrics for Pareto front quality (Hypervolume, IGD, Spread).
* Batch experiments across **20 seeds × 3 parameter sets × 3 instances**.
* Result storage with incremental saving (`results_incremental.pkl`).


### Algorithms
We implement and compare two MOEAs:
* **NSGA-II** (Non-dominated Sorting Genetic Algorithm II)
* **SPEA2** (Strength Pareto Evolutionary Algorithm 2)

The framework evaluates solution quality, convergence, runtime, and diversity across multiple runs and parameter settings, using benchmark instances from CVRPLIB (small, medium, and large).


## Content
* A-n32-k5.vrp
* B-n78-k10.vrp
* X-n101-k25.vrp

* README.md
* main.ipynb # final, executable notebook
* results_experiments.csv
* results_experiments_filled_with_evals.csv
* results_incremental.pkl — incremental log of runs
* reference_front.npy — global Pareto set
* metrics_summary.csv — aggregated metrics

## Requirements
* Python 3.8+
* Libraries:
    * numpy, pandas, matplotlib, seaborn
    * vrplib (to load CVRPLIB.vrp files)
    * ipython (for display styling)
    * scipy

Install (local):
```sh
pip install numpy pandas matplotlib seaborn vrplib ipython scipy
```

## Data (CVRPLIB)
We use three standard CVRPLIB instances:
* **Small**: A-n32-k5.vrp (32 customers, 5 vehicles)
* **Medium**: B-n78-k10.vrp (78 customers, 10 vehicles)
* **Large**: X-n101-k25.vrp (101 customers, 25 vehicles)

These contains:
* Node coordinates (depot + customers)
* Customer demands
* Vehicle capacity


## Quick start
1. Ensure the three `.vrp` files in the same folder as `main.ipynb`.
2. Open and run `main.ipynb`. The notebook will:
    * Load each instance,
    * Build distance matrices,
    * Run `NSGA-II` and `SPEA2` for three parameter sets (pop/gens/pc/pm),
    * Repeat N=20 seeds per (instance × algorithm × param set),
    * Save results incrementally to `results_incremental.pkl`,
    * Build a global reference Pareto set `reference_front.npy`,
    * Compute & save `metrics_summary.csv` (if you run the aggregation section).

3. Use the provided plotting cells to:
    * Compare Pareto fronts per instance/param set,
    * Visualize mean runtime per algorithm,
    * Draw example route maps from any stored Pareto solution,
    * Show boxplots for HV/IGD/Spread by instance and parameter set.
 
 Parameter sets (in the notebook):
 ```sh
 PARAM_SETS = [
    {"pop_size": 100, "gens": 500, "pc": 0.7,  "pm": 0.2},
    {"pop_size": 80,  "gens": 300, "pc": 0.9,  "pm": 0.1},
    {"pop_size": 120, "gens": 600, "pc": 0.8,  "pm": 0.15},
]
 ```

## Implementation notes:
**Representation & Decoding**
* **Genome**: permutation of customer indices (depot excluded).
* **Split**: greedy fill under capacity __Q__; when the next customer would exceed __Q__, start a new route.
* **Route length**: depot -> first -> … -> last -> depot.

**Fitness (objectives)**
* **fitness**(tour, vrp) returns (f1, f2):
* **f1**: total distance (with penalties if any route is overloaded),
* **f2**: std of route lengths.

**Genetic Operators**
* **Initialization**: random permutations.
* **Crossover**: Order Crossover (OX), order-preserving.
* **Mutation**: swap mutation with probability pm per gene.

**MOEA loops**
* **NSGA-II**: vectorized non-dominated sort + crowding distance for selection and environmental survival.
* **SPEA2**: strength/raw/density fitness, external archive, tournament on archive, environmental truncation.


### **Visualization**
####  Experiments:
* Design: 3 instances × 2 algorithms × 3 parameter sets × 20 seeds.
* Logging: after each run, append to results_incremental.pkl:
    * instance, algo, param_set, seed,
    * runtime (s) and evaluation count,
    * full population objectives F,
    * Pareto front PF and its corresponding permutations `PF_routes`.
You can resume experiments; the driver skips runs already present in the incremental file.


#### Metrics & Visualization
* Pareto fronts per instance/param set and aggregated.
* Hypervolume (HV) (2D, minimization, ref = 1.1×worst objective values).
* IGD using the global reference front (reference_front.npy).
* Spread (nearest-neighbor dispersion).
* Runtime summaries (mean ± std) by instance/algorithm/param set.
* Route plots: decode any saved Pareto solution and draw the paths in coordinate space.


### **Known Limitations & Extensions**
* Split/repair is greedy; you can add smarter repair or local search (e.g., 2-opt per route).
* We do not enforce a fixed number of vehicles; the split naturally creates as many as needed under Q. If your assignment version requires exactly K routes, add a route-count repair and/or penalty.
* Penalty coefficient (`1e6`) is coarse; tune if your instances have very large distances.

## Contribution:
The project was done in collaboration with the four members of the group. In the initial phase, the tasks were devided between the members, thereafter in each of the following sessions the codes were reviewed together and then worked on by coordinating via Discord and sharing files on GitHub. Each member contributed to the coding, testing and report written, as well as to the compilation and review of the code by the end of the project.

## Members:
* [Joanne T. Farstad](https://github.com/jofa016) 
* [Robel W. Ghebremedhin](https://github.com/rabrie10)
* [Susrita Khadka](https://github.com/susritak)
* [Karoline Nielsen](https://github.com/karroni)