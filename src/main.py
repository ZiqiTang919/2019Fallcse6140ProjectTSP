import argparse
import sys
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

def read_data(filename):
	file = open(filename)
	for _ in range(5):
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

	return squareform(pdist(X, 'euclidean'))


parser = argparse.ArgumentParser()
parser.add_argument("-inst", dest="filename", required=True)
parser.add_argument("-alg", dest="algorithm", required=True)
parser.add_argument("-time", dest="time", required=True)
parser.add_argument("-seed", dest="seed")

args = parser.parse_args()

distance_matrix = read_data(args.filename)

if args.algorithm == 'BnB':
	best_sol, best_route, trace = BNB(distance_matrix, args.time)
elif args.algorithm == 'Approx':
	best_sol, best_route, trace = MST(distance_matrix, args.time)
elif args.algorithm == 'LS1':
	best_sol, best_route, trace = SA(distance_matrix, args.time, args.seed)
elif args.algorithm == 'LS2':
	best_sol, best_route, trace = ILS(distance_matrix, args.time, args.seed)
else:
	sys.exit('wrong format!')








