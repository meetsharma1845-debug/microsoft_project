import pandas as pd
import threading
import queue
import time
import logging
from typing import List, Dict, Set

# Set up logging for thread tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s'
)

class DependencyAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.graph: Dict[str, List[str]] = {}
        self._load_and_build_graph()

    def _load_and_build_graph(self) -> None:
        try:
            df = pd.read_csv(self.file_path)
            for _, row in df.iterrows():
                source, target = row['source_node'], row['target_node']
                if source not in self.graph:
                    self.graph[source] = []
                self.graph[source].append(target)
            logging.info("Dependency graph built successfully.")
        except Exception as e:
            logging.error(f"Failed to load data: {e}")

    def find_shortest_path_bfs(self, start: str, target: str) -> List[str]:
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
    def __init__(self, analyzer: DependencyAnalyzer, num_threads: int = 3):
        self.analyzer = analyzer
        self.task_queue = queue.Queue()
        self.num_threads = num_threads
        self.threads: List[threading.Thread] = []

    def worker(self) -> None:
        while not self.task_queue.empty():
            task = self.task_queue.get()
            
            # Artificial delay to clearly observe thread behavior
            time.sleep(0.5) 
            
            if task['type'] == 'BFS':
                result = self.analyzer.find_shortest_path_bfs(task['start'], task['target'])
                logging.info(f"BFS Result for {task['name']}: {result}")
            elif task['type'] == 'DFS':
                result = self.analyzer.get_all_dependencies_dfs(task['start'])
                logging.info(f"DFS Result for {task['name']}: {result}")
                
            self.task_queue.task_done()

    def add_task(self, task: dict) -> None:
        self.task_queue.put(task)

    def execute(self) -> None:
        logging.info("Starting thread pool...")
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker, name=f"Worker-{i+1}")
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()
        logging.info("All tasks completed.")

if __name__ == "__main__":
    data_path = "microservices.csv"
    
    analyzer = DependencyAnalyzer(data_path)
    manager = TaskManager(analyzer, num_threads=3)

    # Queue up test queries
    manager.add_task({'name': 'Route Auth to Email', 'type': 'BFS', 'start': 'AuthService', 'target': 'NotificationHub'})
    manager.add_task({'name': 'Audit Frontend downstream', 'type': 'DFS', 'start': 'FrontendAPI', 'target': None})
    manager.add_task({'name': 'Route Frontend to Fraud', 'type': 'BFS', 'start': 'FrontendAPI', 'target': 'FraudDetection'})
    manager.add_task({'name': 'Audit Payment downstream', 'type': 'DFS', 'start': 'PaymentGateway', 'target': None})

    manager.execute()