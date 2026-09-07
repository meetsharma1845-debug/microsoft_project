# Microservice Dependency Analyzer

This project is a multithreaded backend service designed to analyze network topologies and map downstream dependencies in a microservice architecture. It demonstrates proficiency in Object-Oriented Programming (OOP), graph traversal algorithms, and thread-safe concurrency.

## Architecture & Technical Implementation

*   **Data Ingestion (Pandas):** Ingests raw microservice connection data (e.g., API gateways to databases) from a CSV format and constructs a directional adjacency list.
*   **Graph Traversals:**
    *   **Breadth-First Search (BFS):** Calculates the shortest execution path between two specific microservices.
    *   **Depth-First Search (DFS):** Conducts a deep audit of a node to map all direct and indirect downstream dependencies, which is critical for identifying single points of failure.
*   **Concurrency & Deep Threading:** 
    *   Implements a Producer-Consumer architecture using Python's thread-safe `queue.Queue`.
    *   A dynamic pool of worker threads continuously pulls traversal tasks from the queue and executes them concurrently.
*   **Enterprise Standards:** The codebase utilizes Python type hinting for strict data validation and the built-in `logging` module to track thread execution asynchronously.

## Execution
Run `python main.py`. The script will automatically initialize the mock microservice topology, spawn the thread pool, and output timestamped logs of the concurrent traversals.