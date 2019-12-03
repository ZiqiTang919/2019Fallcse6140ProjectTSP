# Introduce Algorithm
# MST Approximation algorithm will use MST to find a tree which has the min cost and contains all of the vertices.
# Then we could use the DFS to find the path of MST tree

# Reference, the DFS and MST are reference from https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
# and geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

import sys
from time import time
from collections import defaultdict

class Graph_DFS(): 
  
    def __init__(self): 
  
        self.graph = defaultdict(list)
        self.graph_path = []
  
    # function to add an edge to graph 
    def add_each_edge(self, u, v): 
        self.graph[u].append(v) 
  
    # A function used by DFS, use recursion to get the DFS path
    def util(self, v, visited):
        # set the current vertex v as visited
        visited[v] = True
        # Then add this vertex into the path
        self.graph_path.append(v)

        for i in self.graph[v]: 
            if visited[i] == False: 
                self.util(i, visited) 
  
    def DFS(self, v): 
  
        # Mark all the vertices as not visited 
        length_graph = len(self.graph)
        # Inintial a list used to store the graph path
        current_visited = [False] * length_graph
        # use the helper funnction to get and update this DFS path
        self.util(v, current_visited)

# This function will be used to calculate the cost for the
# path, which is the ourpur of DFS, add the distance between two consecutive points
# Then add the distance of last vertex and the first vertex, make a cycle, let the travel man get to the start point
def get_cost(matrix, path):
    total_cost = 0
    for i in range(0, len(path) - 1):
        #print(i, i+1)
        total_cost += matrix[path[i]][path[i+1]]

    # add the distance of last vertex and the first vertex, make a cycle, let the travel man get to the start point
    total_cost = total_cost + matrix[path[len(path) - 1]][path[0]]
    #print(len(path) - 1, 0)
    return total_cost

# In this part, we will use MST to find the nodes and paths of the graph G
# Then double every edge of the MST
def MST(distance_array, cutoff_time, seed=None):
    # Set a start time, then when return the time, use
    # the return's time - start time to get the algorithm's runninng time
    start_time = time()

    # Create a DFS vlass as tree, this tree will be used to save the edges of MST
    # also we need to double every edge of the MST
    tree = Graph_DFS()
    # The vertices nunmber of the current city
    vertices_number = len(distance_array.tolist())
    # The array(matrix) pre-calculated, which is the distance between each two vertex in the
    # graph G, then we could use this matrix to calculate the path cost once we get the path from DFS
    distance_array = distance_array.tolist()

    # min_cut will be used to pick minimum weight edge, initial the min_cut[0] to start from the first matrix
    min_cut = [sys.maxsize] * vertices_number
    min_cut[0] = 0

    # This is used to store MST
    mst_temp = [None] * vertices_number
    mst_temp[0] = -1

    set_mst = [False] * vertices_number

    for temp in range(0, vertices_number): 

        min_num = sys.maxsize
        index = 0
        # This is used to find the min distance vertex and
        # then set the current finded vertex into the mst set
        for i in range(0, vertices_number): 
            if (min_cut[i] < min_num and set_mst[i] == False): 
                min_num = min_cut[i] 
                index = i 
        # u is the current min distance vertex
        u = index
        # Set the current vertex u has be visited, cannot be visted again
        set_mst[u] = True

        # this loop is used to tracking the current min distance vertex's adjacent vertices
        for v in range(0, vertices_number):
            # if the current adjacent vertices' distance is larger than the new distance
            # distance_array[u][v], update the distance for the adjacent vertices
            if (distance_array[u][v] > 0 and set_mst[v] == False and min_cut[v] > distance_array[u][v]):
                # update the adjacent vertices' distance
                min_cut[v] = distance_array[u][v] 
                mst_temp[v] = u 

    # double every edge of the MST
    for i in range(1, vertices_number): 
        tree.add_each_edge(mst_temp[i], i)
        tree.add_each_edge(i, mst_temp[i])

    tree.DFS(0)
    cost = get_cost(distance_array, tree.graph_path)

    #trace = time() - start_time
    #trace = float("%0.2f" % (trace))
    
    # The MST Approximation algorithm running time in seconds
    trace = [[time() - start_time, cost]]
    #print(cost, tree.graph_path, trace)
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


