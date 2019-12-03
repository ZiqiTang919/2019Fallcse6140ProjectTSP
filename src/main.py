# main entry of the program
# run the specific algorithm on the given dataset and write running results to outputs

import argparse
import sys
import os

from util import read_data, write_solution, write_trace
from MST import MST
from RHC import RHC
from SA import SA
from BnB import BnB

if __name__ == "__main__":
	# parse command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-inst", dest="filename", required=True)
	parser.add_argument("-alg", dest="algorithm", required=True)
	parser.add_argument("-time", dest="time", required=True)
	parser.add_argument("-seed", dest="seed")

	args = parser.parse_args()

	# compute distance matrix from the input file
	name, distance_matrix = read_data(args.filename)
	outname = '{}_{}_{}'.format(name, args.algorithm, args.time)

	# run the specific algorithm
	if args.algorithm == 'BnB':
		bnb_obj = BnB(distance_matrix, float(args.time))
		bnb_obj.main()
		best_sol = bnb_obj.best_solution
		best_route = bnb_obj.best_route
		trace = bnb_obj.trace
	elif args.algorithm == 'Approx':
		best_sol, best_route, trace = MST(distance_matrix, float(args.time))
	elif args.algorithm == 'LS1':
		best_sol, best_route, trace = SA(distance_matrix, float(args.time), args.seed)
		outname += '_{}'.format(args.seed)
	elif args.algorithm == 'LS2':
		best_sol, best_route, trace = RHC(distance_matrix, float(args.time), args.seed)
		outname += '_{}'.format(args.seed)
	else:
		sys.exit('wrong format!')

	# create output directory
	out_dir_path = 'output/{}/'.format(args.algorithm)
	if not os.path.exists(out_dir_path):
		os.makedirs(out_dir_path)

	# write results to outputs
	write_solution(out_dir_path+outname+'.sol', best_sol, best_route)
	write_trace(out_dir_path+outname+'.trace', trace)








