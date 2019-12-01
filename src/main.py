import argparse
import sys
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import numpy as np

from MST_Approx import *
from RLS import RLS

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
		file.write(str(row[0]) + ',' + str(int(row[1])) + '\n') 

def BNB(distance_matrix, time):
	return None, None, None
'''def MST(distance_matrix, time):
	return None, None, None'''
def SA(distance_matrix, time, seed):
	return None, None, None


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-inst", dest="filename", required=True)
	parser.add_argument("-alg", dest="algorithm", required=True)
	parser.add_argument("-time", dest="time", required=True)
	parser.add_argument("-seed", dest="seed")

	args = parser.parse_args()

	name, distance_matrix = read_data(args.filename)
	outname = '{}_{}_{}'.format(name, args.algorithm, args.time)

	if args.algorithm == 'BnB':
		best_sol, best_route, trace = BNB(distance_matrix, args.time)
	elif args.algorithm == 'Approx':
		best_sol, best_route, trace = MST(distance_matrix, args.time, args.seed)
	elif args.algorithm == 'LS1':
		best_sol, best_route, trace = SA(distance_matrix, args.time, args.seed)
		outname += '_{}'.format(args.seed)
	elif args.algorithm == 'LS2':
		best_sol, best_route, trace = RLS(distance_matrix, args.time, args.seed)
		outname += '_{}'.format(args.seed)
	else:
		sys.exit('wrong format!')

	# best_sol = 1000
	# best_route = [1,2,3,4,5]
	# trace = [[10, 1111], [50, 1100], [100, 1000]]

	write_solution(outname+'.sol', best_sol, best_route)
	write_trace(outname+'.trace', trace)







