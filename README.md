# Taxi-Station-System-Project

## Introduction

In this exercise, I take the role of the owner of a taxi business. My objective is to efficiently deliver passengers to their destinations using search algorithms.

## Environment

The environment is represented as a rectangular grid, where each grid cell corresponds to an area. Areas can be either passable or impassable for taxis. Passengers, waiting to be transported, are scattered across the grid, along with gas stations where taxis can refuel.
The files: check.py, search.py, utils.py are given. The implemenation of the task is in ex1.py.

## Actions

1. **Move**: Taxis can move one tile vertically or horizontally, but not diagonally. Movement consumes 1 unit of fuel and is only possible when the taxi has fuel. Syntax: `("move", "taxi_name", (x, y))`

2. **Pick Up**: Taxis can pick up passengers if they are on the same tile. The number of passengers in a taxi cannot exceed its capacity. Syntax: `("pick up", "taxi_name", "passenger_name")`

3. **Drop Off**: Taxis can drop off passengers only at their destination tile. Syntax: `("drop off", "taxi_name", "passenger_name")`

4. **Refuel**: Taxis can refuel at gas stations, restoring their fuel to maximum capacity. Syntax: `("refuel", "taxi_name")`

5. **Wait**: Taxis can choose to wait, not changing their state. Syntax: `("wait", "taxi_name")`

## Additional Rules

- Taxis start empty with full tanks, positioned on passable tiles.
- Only one taxi can be on a tile at a time.
- Some problems may be unsolvable due to impassable terrain, fuel shortages, lack of connectivity, etc.

## Goal

The goal is to deliver every passenger to their destination in the shortest number of turns.

## Task Implementaion

The input is dictionary describing the initial environment, including the grid, taxi details, and passenger information.Functions that i implemented in the `TaxiProblem` class to facilitate the search:

- `actions(self, state)`: Returns available actions from a given state.
- `result(self, state, action)`: Returns the next state given the previous state and an action.
- `goal_test(self, state)`: Checks if a given state is a goal state.
- `h(self, node)`: Computes an admissible heuristic estimate for a node.
- `h_1(self, node)`: A simple heuristic function.
- `h_2(self, node)`: A more complex heuristic function.

## Solution

When running `check.py` with various inputs. Outputs may include:
- A bug (self-explanatory).
- `(-2, -2, None)`: No solution found, either due to unsolvability or a timeout.
- A solution: A list of actions taken, runtime, and the number of turns.


