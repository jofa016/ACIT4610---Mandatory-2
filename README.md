# **ACIT 4610 – Mid-Term Portfolio Project 1**
## Vehicle Routing Problem (VRP) with a Quantum-Inspired Genetic Algorithm
### Group 4
This repository solves small/medium/large Vehicle Routing Problem (VRP) instances using Genetic Algorithm (GA) with a “**quantum-inspired**” split representation:
* Genome: a permutation of customers
* route cuts: a companion boolean vector that decides where to split the permutation into routes

It then evaluates solution quality, convergence, runtime, and consistency across multiple runs and parameter sets.


## Changes/Missing:

### Data & Constraints
- [ ] Add customer demands array (demands) from CVRPLIB.
- [ ] Add vehicle capacity Q.
- [ ] Implement route_load(route, demands) to compute total demand per route.

### Repair & Feasibility
- [ ] Implement greedy capacity repair (split overloaded routes, merge/split to match V).
- [ ] Add capacity_violation(...) to quantify infeasibility.
- [ ] Integrate repair into offspring creation (after crossover/mutation).

### Objectives
- [ ] Add second objective (route imbalance: max route length or std. deviation).
- [ ] Replace fitness() with objective_vector(...) that returns (f1, f2).

### MOEAs
- [ ] Implement NSGA-II loop (non-dominated sorting, crowding distance, Pareto-based selection).
- [ ] Implement a second MOEA - SPEA2.

### Experiments
- [ ] Load CVRPLIB instances.
    - Small: A-n32-k5 (32 customers, 5 vehicles). 
    - Medium: B-n78-k10 (78 customers, 10 vehicles). 
    - Large: X-n101-k25 (101 customers, 25 vehicles). 
- [ ] Define three parameter sets (pop size, generations, pc, pm).
- [ ] Run each setting ≥20 times for statistical reliability.

### Analysis & Reporting
- [ ] Extract and plot Pareto fronts (f1 vs f2).
- [ ] Compute at least one convergence/diversity metric (Hypervolume, GD, or Spread).
- [ ] Tabulate mean/Best/Worst runtime and metrics across runs.
- [ ] Write up report comparing two MOEAs, parameter effects, and results.



## Content
* README.md
* MAIN_CODE_BHF.ipynb # final, executable notebook
* customers.csv # data of costumers locations
* results.csv

## Requirements
* Python 3.8+
* Libraries:
    * numpy
    * pandas
    * matplotlib
    * ipython (for display styling)

Install (local):
```sh
pip install numpy pandas matplotlib ipython
```

## Data Format (CSV)
The code uses a csv with the folowing columns:
> id,x,y 

In wich id represent the costumers id, and x, y the coordinates of their homes/location. And by discussion it got decided that the center of all would be the depot location.



## Quick start
1. Ensure costumers.csv is in the same folder as the MAIN_CODE
2. In the notebook, make sure you load with a relative path that works for you:

```sh
df = pd.read_csv("customers.csv")  # not "/customers.csv"
``` 
```sh
df = pd.read_csv("./customers.csv")
```
```sh
df = pd.read_csv("data/customers.csv")
```
```sh
df = pd.read_csv("/content/customers.csv")
```

3. Run all cells. The notebook will produce:
* results.csv
* table_solution_quality.csv
* table_computational_efficiency.csv
* table_convergence_rate.csv
 

## GA Overview:
- **Representation:** A customer **order** (permutation) + a **cut list / split vector** that marks where each new vehicle route starts.
- **Initialization:** Start with random orders and random cuts.
- **Decoding & repair:** Turn the order + cuts into routes; if any route exceeds capacity, move the last customers to the next route(s) until all are feasible.
- **Crossover:** Order-preserving crossover for the permutation; element-wise blend for the splits, then **repair** so there are exactly **V−1** cuts.
- **Mutation:** Small random changes—swap or insert a customer; flip or nudge a cut (±1)—then repair to keep the solution valid.
- **Selection:** k-tournament (**k = 3**) or rank-based (higher-ranked individuals are picked more often).
- **Elitism:** Copy the top **K** (~1–5% of the population) directly into the next generation.
- **Fitness:** Shorter total distance (depot → customers → depot per route) is better. The GA maximizes **−distance**; optional penalties can discourage capacity or route-count violations.

## Implementation notes:
### **Instances**
We build several VRP instances (Small/Medium/Large) within the numbers provided in the task and having two different instances within each sizes.

```sh
class VRPInstance:
    def __init__(self, depot, vehicles, customers):
        self.depot = depot
        self.customers = customers
        self.vehicles = vehicles
```

### **Representation**
Each solution is an `individual(perm, cuts)`
* `perm`: permutation of costumers IDs(1..N)
* `cuts`: sorted index by where we split perm into routes(size = V-1)

```sh
class Individual(NamedTuple):
    perm: List[int]
    cuts: List[int]
```
### **Decoding and cost**
* Decoding routes by slicing `perm` at `cuts`; compute route cost as depot → route → depot.

```sh
def decode_routes(ind: Individual, V:int) -> List[List[int]]:
```
*  Route/total distance:
```sh   
def route_distance(route: List[int], dmat) -> float: 
def total_distance(ind: Individual, dmat, V: int) -> float:
```   

### **Fitness**
We want to minimize total distance, while the GA maximizes fitness; `fitness = −(total distance + penalties)` maximizing fitness = minimizing distance.

```sh
def fitness(ind: Individual, dmat, V: int) -> float:
    return -total_distance(ind, dmat, V)
```

### **Selection**
k-tournment by default (k=3); sample 3 candidates and keep the best; rank-based selection is also available (samples by rank, not raw fitness).

```sh
def tournament_selection_idx(fitnesses: List[float], k: int, rng: random.Random) -> int:
    cand = [rng.randrange(len(fitnesses)) for i in range(k)]
    return max(cand, key=lambda i: fitnesses[i])
```

### **Crossover**
* **Permutation (order-preserving OX):** keeps the relative visit order intact.
* **Splits (element-wise blend + repair):** mixes cut positions, then repairs to ensure exactly **V−1** valid cuts.

```sh
def order_crossover(p1: List[int], p2: List[int], rng: random.Random) -> Tuple[List[int], List[int]]:
```

```sh
def cuts_crossover(c1: List[int], c2: List[int], N: int, V: int, rng: random.Random) -> Tuple[List[int], List[int]]:
```

```sh
def repair_cuts(cuts: List[int], N: int, V:int, rng: random.Random) -> List[int]:
```

### **Mutation**
* **Permutation:** swap or insert a random customer.
* **Splits:** bit-flip or ±1 jitter on a cut, followed by `repair_cuts`.

```sh
def swap_mutation_perm(p: List[int], p_mut:float, rng: random.Random) -> List[int]:
```
```sh
def jitter_mutation_cuts(cuts: List[int], N:int, V:int, p_mut: float, rng: random.Random) -> List[int]:
```

### **GA engine (loop)**
* Initialize population → repeat **{selection → crossover → mutation → evaluation}** for the set number of generations.
* **Elitism (optional):** copy top-K (~1–5%) directly into the next generation.

```sh
best_ind, best_dist, best_hist = genetic_algorithm(dmat, N=len(instance.customers), V=instance.vehicles, pop_size=120, generations=20, k_tourn=3, pc=0.9, pm_perm=0.2, pm_cuts=0.2, seed=42, log_convergence=True)
```

### **Visualization**
Visualize routes for each instance
```sh
def plot_routes(ind, customers, depot, n_vehicles, number_points=False, title=None):
```

####  Batch experiments and metrics:
* Parameter sets:
```sh
param_sets = {
    "Balanced":   {"pop_size": 50,  "generations": 200, "k_tourn": 3, "pc": 0.7,  "pm_perm": 0.01,  "pm_cuts": 0.1},
    "High exploration":  {"pop_size": 150, "generations": 500, "k_tourn": 3, "pc": 0.85, "pm_perm": 0.05,  "pm_cuts": 0.2},
    "Focus exploitation": {"pop_size": 20,  "generations": 100, "k_tourn": 3, "pc": 0.6,  "pm_perm": 0.005, "pm_cuts": 0.5},
}

n_runs = 20
```
* For each instance × parameter set × seed, we record: Best distance, runtime, history (for convergence).
 
* saved objects:
    * `results.csv` (summary)
    * `table_solution_quality.csv`
    * `table_convergence_rate.csv`
    * `table_computational_efficiency.csv`

### **Reproducibility & Performance**
* Seeds: set `seed` for repeatability; use `n_runs > 1` to report mean ± std.
* Runtime: fitness evaluation dominates; precompute distance matrix; start with smaller `pop_size/generations` and scale.

### **Known Limitations & Extensions**
*  Capacity handling is basic; add capacity-aware splitting + greedy repair if needed.
* Add 2-opt per route; compare with OR-Tools for a baseline.

## Contribution:
The project was done in collaboration with the four members of the group. In the initial phase, the tasks were devided between the members, thereafter in each of the following sessions the codes were reviewed together and then worked on by coordinating via Discord and sharing files on GitHub. Each member contributed to the coding, testing and report written, as well as to the compilation and review of the code by the end of the project.

## Members:
* [Joanne T. Farstad](https://github.com/jofa016) 
* [Robel W. Ghebremedhin](https://github.com/rabrie10)
* [Susrita Khadka](https://github.com/susritak)
* [Karoline Nielsen](https://github.com/karroni)