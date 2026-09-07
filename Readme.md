# Multithreaded Network Dependency Analyzer

This project simulates a backend service that analyzes a network of connected nodes and processes multiple analytical queries concurrently. It was built to demonstrate proficiency in data handling, graph traversal, and advanced concurrency.

## Core Requirements Implemented

*   **Pandas:** Used for data ingestion. The program reads raw node-connection data from a CSV file and processes it into an adjacency list (graph dictionary) for rapid querying.
*   **Traversal Trees (BFS & DFS):** 
    *   **BFS (Breadth-First Search):** Implemented to calculate the absolute shortest path between two specific nodes.
    *   **DFS (Depth-First Search):** Implemented to map out all direct and indirect downstream connections from a starting node.
*   **Deep Threading (Producer-Consumer Architecture):** Utilized Python's `queue.Queue` to build a thread-safe task pipeline. A main thread acts as the producer, feeding specific traversal queries into the queue.
*   **Multithreading:** Created a pool of concurrent Worker threads that continuously pull from the thread-safe queue and execute the BFS/DFS algorithms simultaneously without race conditions.

## How to Run
1. Ensure Pandas is installed (`pip install pandas`).
2. Run `python main.py`. 
3. The script will automatically generate the mock CSV dataset, build the graph, and trigger the multithreaded workers to solve the queries concurrently.