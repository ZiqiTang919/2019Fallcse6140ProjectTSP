# restart local search with opt-2 exchange

from time import time
import numpy as np

def init_route(distance_matrix):
	N = len(distance_matrix)
	route = np.random.permutation(N)
	val = 0
	for i in range(N):
		val += distance_matrix[route[i-1]][route[i]]

	return val, route

def search_neighbors(distance_matrix, curr_val, curr_route):
	N = len(distance_matrix)
	best_val, best_route = curr_val, curr_route[:]
	for i in range(N-2):
		for j in range(i+2, min(N, N - 1 + i)):
			new_val = curr_val - distance_matrix[curr_route[i-1]][curr_route[i]] - distance_matrix[curr_route[j-1]][curr_route[j]]
			new_val += distance_matrix[curr_route[i-1]][curr_route[j-1]] + distance_matrix[curr_route[i]][curr_route[j]]

			if new_val < best_val:
				best_val = new_val
				best_route = np.concatenate((curr_route[0:i], curr_route[i:j][::-1], curr_route[j:]))

	return best_val, best_route

def RLS(distance_matrix, cutoff, seed):
	start_time = time()
	cutoff = float(cutoff)

	np.random.seed(int(seed))

	curr_val, curr_route = init_route(distance_matrix)
	trace = [[time() - start_time, curr_val]]
	best_val, best_route = curr_val, curr_route[:]
	global_best_val, global_best_route = best_val, best_route[:]

	it = 0
	max_not_improve = 20

	while it < max_not_improve:
		curr_val, curr_route = search_neighbors(distance_matrix, curr_val, curr_route)
		
		if time() - start_time > cutoff:
			break

		if curr_val < best_val:
			best_val, best_route = curr_val, curr_route[:]
			if curr_val < global_best_val:
				global_best_val, global_best_route = curr_val, curr_route[:]
				trace.append([time() - start_time, curr_val])
				it = 0
		else:
			curr_val, curr_route = init_route(distance_matrix)
			best_val, best_route = curr_val, curr_route[:]
			it += 1

	print('total time: ', time() - start_time, 'best val: ', int(global_best_val))
	return global_best_val, global_best_route, trace
