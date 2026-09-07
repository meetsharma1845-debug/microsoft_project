import pandas as pd

# 1 & 2. Create and load the data (added Eve and Frank)
file_path = r"c:\Users\MEET\OneDrive\Desktop\microsoft project\friends.csv"
data = "person1,person2\nAlice,Bob\nBob,Charlie\nCharlie,David\nAlice,Eve\nEve,Frank\n"

with open(file_path, "w") as f:
    f.write(data)

df = pd.read_csv(file_path)

# 3. Turn the Pandas table into a "Network Web" (Graph Dictionary)
network = {}
for index, row in df.iterrows():
    p1 = row['person1']
    p2 = row['person2']
    if p1 not in network:
        network[p1] = []
    network[p1].append(p2)

# 4. The BFS Detective (Shortest path)
def find_shortest_path(graph, start, target):
    queue = [[start]] 
    visited = set()   
    while queue:
        path = queue.pop(0) 
        person = path[-1]   
        if person == target:
            return path     
        if person not in visited:
            visited.add(person)
            for friend in graph.get(person, []):
                new_path = list(path)
                new_path.append(friend)
                queue.append(new_path)
    return "No connection found"

# 5. The DFS Detective (Deep Dive to find ALL connections)
def get_all_connections_dfs(graph, start):
    stack = [start] # A stack of people to check
    visited = set()
    
    while stack:
        person = stack.pop() # Grab the LAST person added (dives deep instantly)
        if person not in visited:
            visited.add(person)
            # Add their friends to the stack
            for friend in graph.get(person, []):
                stack.append(friend)
                
    return list(visited)

# Let's test both detectives!
print("BFS: Shortest path from Alice to David:")
print(find_shortest_path(network, "Alice", "David"))

print("\nDFS: Everyone Alice is connected to (directly or indirectly):")
print(get_all_connections_dfs(network, "Alice"))