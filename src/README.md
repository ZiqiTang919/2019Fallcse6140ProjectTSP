Authors            : Xinyi Zhang, Jingyi Li, Yuxin Zhou, Ziqi Tang
Created            : November 1, 2019
Last Modified   : December 3, 2019
Affiliation          : Georgia Institute of Technology

Description
-------------
This project implements four algorithms (branch-and-bound, minimum spanning tree heuristic, sinulated annealing, and restart hill climbing) to solve the Travelling Salesman Problem. 

The overall structure is:

main.py: test file for running an algorithm on a given input dataset.
BnB.py: implements branch-and-bound algorithm.
MST.py: implements minimum spanning tree heuristic.
SA.py: implements local search using sinulated annealing.
RHC.py: implements local search using restart hill climbing.
util.py: util functions for reading dataset and writing outputs.


Execution
-----------
To run the algorithms, please go to the directory /code , then run     

    python main.py -inst <file_path> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]

where <file_path> is the path of the input data file to be read (see bellow for specific format),
the -alg [BnB | Approx | LS1 | LS2] tag specifies the algorithm to be run (LS1 for SA and LS2 for RHC),
<cutoff_in_seconds> is the time limit for running the program,
<random_seed> is an optional argument to set the random seed for local search algorithms.

The program will run the specified algorithm on the given dataset, two result files will be stored in the directort /output . The first output is the solution file which contains the quality of best solution found and the corresponding TSP route. The second output is the solution traces file which contains a list of timestamps and the quality of best solution found at that time.


Input Data Format
------------
The data file contains N points represent specific locations in some city.
The first 5 lines include information about the dataset.
The following N lines represent N points coordinates. 
Each line has three components (space split): NODE_ID  X_COORD  and  Y_COORD 

The file should be like this:

NAME: Atlanta
COMMENT: 20 locations in Atlanta
DIMENSION: 20
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 33665568.000000 -84422070.000000
2 33764940.000000 -84371819.000000
3 33770889.000000 -84358622.000000
...


