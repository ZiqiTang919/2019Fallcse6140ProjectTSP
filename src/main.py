import argparse
import sys
import os

from util import read_data, write_solution, write_trace
from MST_Approx import *
from RLS import RLS
from SA import SA
import bnb

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
		bnb_obj = bnb.BnB(distance_matrix, float(args.time))
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
		best_sol, best_route, trace = RLS(distance_matrix, float(args.time), args.seed)
		outname += '_{}'.format(args.seed)
	else:
		sys.exit('wrong format!')

	out_dir_path = 'output/{}/'.format(args.algorithm)
	if not os.path.exists(out_dir_path):
		os.makedirs(out_dir_path)

	write_solution(out_dir_path+outname+'.sol', best_sol, best_route)
	write_trace(out_dir_path+outname+'.trace', trace)








