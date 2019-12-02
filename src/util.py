from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import numpy as np

def read_data(filename):
	file = open(filename, 'r')
	line = file.readline()
	name = line.split(' ')[-1][:-1]
	for _ in range(4):
		file.readline()
	
	X = []
	ids = []
	while True:
		line = file.readline()
		if line.startswith('EOF'):
			break
		line = line.split(' ')
		x = float(line[1])
		y = float(line[2])
		X.append([x, y])

	return name, np.round(squareform(pdist(X, 'euclidean')) + 1e-9)

def write_solution(filename, sol, route):
	file = open(filename, 'w')
	file.write(str(int(sol)) + '\n')
	file.write(','.join([str(v) for v in route])) 

def write_trace(filename, trace):
	file = open(filename, 'w')
	for row in trace:
		file.write('{:.2f},{}\n'.format(np.round(row[0], 2), int(row[1])))