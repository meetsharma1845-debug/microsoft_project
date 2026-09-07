import pandas as pd
import threading
import queue
import time

# 1. Create and load the data
file_path = r"c:\Users\MEET\OneDrive\Desktop\microsoft project\friends.csv"
data = "person1,person2\nAlice,Bob\nBob,Charlie\nCharlie,David\nAlice,Eve\nEve,Frank\n"

with open(file_path, "w") as f:
    f.write(data)

df = pd.read_csv(file_path)

# 2. Build the Network Web
network = {}
for index, row in df.iterrows():
    p1 = row['person1']
    p2 = row['person2']
    if p1 not in network:
        network[p1] = []
    network[p1].append(p2)

# 3. BFS Detective (Shortest path)
def find_shortest_path(graph, start, target):
    q = [[start]]
    visited = set()
    while q:
        path = q.pop(0)
        person = path[-1]
        if person == target:
            return path
        if person not in visited:
            visited.add(person)
            for friend in graph.get(person, []):
                new_path = list(path)
                new_path.append(friend)
                q.append(new_path)
    return []

# 4. DFS Detective (Deep Dive)
def get_all_connections_dfs(graph, start):
    stack = [start]
    visited = set()
    while stack:
        person = stack.pop()
        if person not in visited:
            visited.add(person)
            for friend in graph.get(person, []):
                stack.append(friend)
    return list(visited)

# 5. NEW: MULTITHREADING & DEEP THREADING
task_queue = queue.Queue()

def worker_detective(worker_name):
    while not task_queue.empty():
        task = task_queue.get()
        print(f"[{worker_name}] Starting task: {task['task_name']}")
        
        time.sleep(1) 
        
        if task['type'] == 'BFS':
            result = find_shortest_path(network, task['start'], task['target'])
            print(f"   -> [{worker_name}] Solved BFS! Path: {result}")
        elif task['type'] == 'DFS':
            result = get_all_connections_dfs(network, task['start'])
            print(f"   -> [{worker_name}] Solved DFS! Connections: {result}")
            
        task_queue.task_done()

task_queue.put({'task_name': 'Find path Alice to David', 'type': 'BFS', 'start': 'Alice', 'target': 'David'})
task_queue.put({'task_name': 'Find all Eve connections', 'type': 'DFS', 'start': 'Eve', 'target': None})
task_queue.put({'task_name': 'Find path Bob to Frank', 'type': 'BFS', 'start': 'Bob', 'target': 'Frank'})
task_queue.put({'task_name': 'Find all Alice connections', 'type': 'DFS', 'start': 'Alice', 'target': None})

print("Boss finished putting tasks in the box. Waking up the workers...\n")

threads = []
for i in range(3):
    worker_name = f"Detective-{i+1}"
    t = threading.Thread(target=worker_detective, args=(worker_name,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nAll tasks completed! We are done.")