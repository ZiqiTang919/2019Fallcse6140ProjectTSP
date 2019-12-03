# implements restart hill climbing with 2-opt exchange

from time import time
import numpy as np

# given the distance matrix, randomly return a vertex permutation as the initial route and the corresponding cost

def init_route(distance_matrix):
	N = len(distance_matrix)
	route = np.random.permutation(N)
	val = 0
	for i in range(N):
		val += distance_matrix[route[i-1]][route[i]]

	return val, route

# using 2-opt exchange to explore neighbors and return the neighbor with the lowest cost

def search_neighbors(distance_matrix, curr_val, curr_route):
	N = len(distance_matrix)
	best_val, best_route = curr_val, curr_route[:]
	# enumrate all neighbors i, j are the endpoints of two edges to be broken and reconnected
	for i in range(N-2):
		for j in range(i+2, min(N, N - 1 + i)):
			new_val = curr_val - distance_matrix[curr_route[i-1]][curr_route[i]] - distance_matrix[curr_route[j-1]][curr_route[j]]
			new_val += distance_matrix[curr_route[i-1]][curr_route[j-1]] + distance_matrix[curr_route[i]][curr_route[j]]

			if new_val < best_val:
				best_val = new_val
				best_route = np.concatenate((curr_route[0:i], curr_route[i:j][::-1], curr_route[j:]))

	return best_val, best_route

# Restart Hill Climbing funciton

# the function perform Hill Climbing with multiple random restarts untill the termination
# termination conditions are: 1. running time exceeds the cutoff; 2. no improvement on best solution after X number of restarts
# seed is used to set the random seed
# the function will return three variables:
# 1. the quality of the best found solution
# 2. the corresponding TSP route as a list of vertex
# 3. the trace of best found solutions and timestamps

def RHC(distance_matrix, cutoff, seed):
	start_time = time()

	np.random.seed(int(seed))

	curr_val, curr_route = init_route(distance_matrix)
	trace = [[time() - start_time, curr_val]]

	# best quality found in each hill climbing iteration
	best_val, best_route = curr_val, curr_route[:]
	# global best quality in whole program
	global_best_val, global_best_route = best_val, best_route[:]

	it = 0
	max_not_improve = 20

	while it < max_not_improve:
		# jump to the best neighbor
		curr_val, curr_route = search_neighbors(distance_matrix, curr_val, curr_route)
		
		# terminate when reach the time limit
		if time() - start_time > cutoff:
			break

		# update the best quality found in current hill climbing
		if curr_val < best_val:
			best_val, best_route = curr_val, curr_route[:]
			# update the overall best quality
			if curr_val < global_best_val:
				global_best_val, global_best_route = curr_val, curr_route[:]
				trace.append([time() - start_time, curr_val])
				# made improvement, reset the iteration counter
				it = 0
		# has reached the local optima, randomly restarts
		else:
			curr_val, curr_route = init_route(distance_matrix)
			best_val, best_route = curr_val, curr_route[:]
			# no improvement, increment the counter by 1
			it += 1

	# print('total time: ', time() - start_time, 'best val: ', int(global_best_val))
	return global_best_val, global_best_route, trace
