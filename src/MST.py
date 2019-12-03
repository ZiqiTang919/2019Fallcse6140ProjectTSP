import sys
from time import time
from collections import defaultdict
#from util import *
  
# This part, we implement a MST to get a tree, which connects all
# vertices in G to be together

# def find_MST():


class Graph_DFS(): 
  
    def __init__(self): 
  
        self.graph = defaultdict(list)
        self.graph_path = []
  
    # function to add an edge to graph 
    def addEdge(self, u, v): 
        self.graph[u].append(v) 
  
    # A function used by DFS 
    def DFSUtil(self, v, visited): 
  
        visited[v] = True
        self.graph_path.append(v)
        #print(self.graph_path)
  
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.DFSUtil(i, visited) 
  
    def DFS(self, v): 
  
        # Mark all the vertices as not visited 
        visited = [False] * (len(self.graph)) 
  
        self.DFSUtil(v, visited)

def get_cost(matrix, path):
    total_cost = 0
    for i in range(0, len(path) - 1):
        #print(i, i+1)
        total_cost += matrix[path[i]][path[i+1]]

    total_cost = total_cost + matrix[path[len(path) - 1]][path[0]]
    #print(len(path) - 1, 0)
    return total_cost


def MST(distance_array, cutoff_time, seed=None):
    start_time = time()

    tree = Graph_DFS()
    vertices_number = len(distance_array.tolist())
    distance_array = distance_array.tolist()

    key = [sys.maxsize] * vertices_number
    parent = [None] * vertices_number

    key[0] = 0 
    mstSet = [False] * vertices_number

    parent[0] = -1

    for cout in range(0, vertices_number): 

        min_num = sys.maxsize
        min_index = 0
        for v in range(0, vertices_number): 
            if key[v] < min_num and mstSet[v] == False: 
                min_num = key[v] 
                min_index = v 

        u = min_index
        mstSet[u] = True

        for v in range(0, vertices_number): 
            if distance_array[u][v] > 0 and mstSet[v] == False and key[v] > distance_array[u][v]: 
                    key[v] = distance_array[u][v] 
                    parent[v] = u 

    #self.printMST(parent)
    for i in range(1, vertices_number): 
        #print parent[i], "-", i, "\t", self.graph[i][ parent[i] ]
        tree.addEdge(parent[i], i)
        tree.addEdge(i, parent[i])

    tree.DFS(0)
    cost = get_cost(distance_array, tree.graph_path)

    #trace = time() - start_time
    #trace = float("%0.2f" % (trace))
    trace = [[time() - start_time, cost]]
    print(cost, tree.graph_path, trace)
    return cost, tree.graph_path, trace
    #return tree

'''def main():
    start_time = time()
    name, dist_array = read_data('Atlanta.tsp')
    tree = MST(len(dist_array.tolist()), dist_array.tolist())
    tree.DFS(0)

    cost = get_cost(dist_array.tolist(), tree.graph_path)

    #trace = time() - start_time
    #trace = float("%0.2f" % (trace))
    trace = [[time() - start_time, cost]]
    print(cost, tree.graph_path, trace)
    return cost, tree.graph_path, trace
  
if __name__== "__main__":
    main()'''





