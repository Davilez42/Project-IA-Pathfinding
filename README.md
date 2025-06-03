# Proyecto 1 - IA

This project implements two essential pathfinding algorithms used in artificial intelligence and graph traversal: **A\*** (A-star) and **Breadth-First Search (BFS)**. It is designed to help visualize and compare how these algorithms find paths from a start point to a goal within a grid-based environment.

## 📌 Overview

- ✅ **A\***: An informed search algorithm that uses a heuristic to efficiently find the shortest path.
- ✅ **BFS**: An uninformed algorithm that guarantees the shortest path in unweighted graphs.
- 🧱 Supports obstacles, walls, and customizable maps.
- 🎯 Highlights explored nodes and final paths step-by-step.
- 📊 Compares performance metrics such as visited nodes and path cost.

## 🧠 Algorithms

### A* Search
- Uses a combination of actual cost (`g(n)`) and estimated cost (`h(n)`) to guide search.
- Supports heuristics like Manhattan or Euclidean distance.
- Ideal for shortest-path problems with weights or obstacles.

### Breadth-First Search (BFS)
- Explores all neighbors at the current depth before moving deeper.
- Guarantees the shortest path in unweighted graphs.
- Easy to implement and understand.



## Instalation

```bash
  pip install -r requirements.txt
  cd src
  python GUI.py
```
