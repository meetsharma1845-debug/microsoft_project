import pandas as pd
import threading
import queue
import time
import logging
from typing import List, Dict, Set

# Configure professional logging to track concurrent threads
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s'
)

class DependencyAnalyzer:
    """Analyzes network dependencies using Pandas and Graph Traversals."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.graph: Dict[str, List[str]] = {}
        self._load_and_build_graph()

    def _load_and_build_graph(self) -> None:
        """Loads data via Pandas and constructs the adjacency list."""
        try:
            df = pd.read_csv(self.file_path)
            for _, row in df.iterrows():
                source, target = row['source_node'], row['target_node']
                if source not in self.graph:
                    self.graph[source] = []
                self.graph[source].append(target)
            logging.info("Successfully loaded data and built dependency graph.")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")

    def find_shortest_path_bfs(self, start: str, target: str) -> List[str]:
        """Finds the shortest path between two nodes using Breadth-First Search."""
        if start not in self.graph:
            return []
            
        q = [[start]]
        visited: Set[str] = set()
        
        while q:
            path = q.pop(0)
            node = path[-1]
            
            if node == target:
                return path
                
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    new_path = list(path)
                    new_path.append(neighbor)
                    q.append(new_path)
        return []

    def get_all_dependencies_dfs(self, start: str) -> List[str]:
        """Maps all downstream dependencies using Depth-First Search."""
        if start not in self.graph:
            return []
            
        stack = [start]
        visited: Set[str] = set()
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    stack.append(neighbor)
        return list(visited)

class TaskManager:
    """Handles deep threading and concurrency for network analysis."""
    
    def __init__(self, analyzer: DependencyAnalyzer, num_threads: int = 3):
        self.analyzer = analyzer
        self.task_queue = queue.Queue()
        self.num_threads = num_threads
        self.threads: List[threading.Thread] = []

    def worker(self) -> None:
        """Worker thread logic to process queue tasks."""
        while not self.task_queue.empty():
            task = self.task_queue.get()
            logging.info(f"Processing task: {task['name']}")
            
            # Simulate processing time for thread observation
            time.sleep(0.5) 
            
            if task['type'] == 'BFS':
                result = self.analyzer.find_shortest_path_bfs(task['start'], task['target'])
                logging.info(f"BFS Result for {task['name']}: {result}")
            elif task['type'] == 'DFS':
                result = self.analyzer.get_all_dependencies_dfs(task['start'])
                logging.info(f"DFS Result for {task['name']}: {result}")
                
            self.task_queue.task_done()

    def add_task(self, task: dict) -> None:
        """Producer method to queue analysis tasks."""
        self.task_queue.put(task)

    def execute(self) -> None:
        """Spawns workers and executes all tasks concurrently."""
        logging.info("Starting thread pool execution...")
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker, name=f"Worker-{i+1}")
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()
        logging.info("All tasks completed successfully.")

if __name__ == "__main__":
    # 1. Generate professional mock dataset (Microservice Architecture)
    data_path = "microservices.csv"
    mock_data = (
        "source_node,target_node\n"
        "AuthService,UserDatabase\n"
        "PaymentGateway,FraudDetection\n"
        "FrontendAPI,AuthService\n"
        "FrontendAPI,PaymentGateway\n"
        "AuthService,EmailService\n"
        "EmailService,NotificationHub\n"
    )
    with open(data_path, "w") as f:
        f.write(mock_data)

    # 2. Initialize the core analyzer
    analyzer = DependencyAnalyzer(data_path)

    # 3. Setup the Multithreaded Task Manager
    manager = TaskManager(analyzer, num_threads=3)

    # 4. Load professional queries into the thread-safe queue
    manager.add_task({'name': 'Route Auth to Email', 'type': 'BFS', 'start': 'AuthService', 'target': 'NotificationHub'})
    manager.add_task({'name': 'Audit Frontend downstream', 'type': 'DFS', 'start': 'FrontendAPI', 'target': None})
    manager.add_task({'name': 'Route Frontend to Fraud', 'type': 'BFS', 'start': 'FrontendAPI', 'target': 'FraudDetection'})
    manager.add_task({'name': 'Audit Payment downstream', 'type': 'DFS', 'start': 'PaymentGateway', 'target': None})

    # 5. Execute concurrently
    manager.execute()