# Network Dependency Analyzer

A multithreaded backend tool built to analyze network topologies and map out dependencies in a mock microservice architecture. 

## Features
*   **Data Ingestion:** Uses Pandas to load node-connection data from `microservices.csv` and builds an adjacency list.
*   **Graph Traversals:**
    *   **BFS:** Finds the shortest execution path between two given microservices.
    *   **DFS:** Maps all direct and indirect downstream dependencies from a starting node to audit potential failure points.
*   **Concurrency:** Uses a thread-safe `queue.Queue` to manage tasks. A pool of worker threads pulls from the queue to run multiple BFS/DFS queries simultaneously without race conditions.

## How to Run
1. Install dependencies: `pip install pandas`
2. Run the script: `python main.py`
The terminal will output timestamped thread logs showing the workers executing the queries concurrently.