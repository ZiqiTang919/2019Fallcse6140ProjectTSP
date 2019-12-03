import random
import math
import time
import numpy as np


def opt2(curr_route, cost_matrix):
    i = 0
    j = 0
    while abs(i - j) < 2:
        i = random.randint(0, len(cost_matrix))
        j = random.randint(0, len(cost_matrix))

    if i > j:
        i, j = j, i
    new_route = np.concatenate((curr_route[0:i], curr_route[i:j][::-1], curr_route[j:]))
    return new_route


def cost(route, cost_matrix):
    cost = 0
    for i in range(len(cost_matrix)):
        cost += cost_matrix[route[i - 1]][route[i]]
    return cost


def probability(new_cost, curr_cost, temperature):
    delta = (new_cost - curr_cost)
    if delta <= 0:
        return 1
    else:
        return math.exp(-delta/temperature)


def cooling_procedure(temp, para):
    while True:
        temp *= para
        yield temp
        if temp < 1e-6:
            break

def SA(cost_matrix, cutoff, seed):
    stime = time.clock()
    temp = 10000
    best_result = float('inf')
    best_route = None
    trace = []
    para = 0.9997
    random.seed(seed)

    curr_route = np.array(random.sample(range(0, cost_matrix.shape[0]),cost_matrix.shape[0]))

    for temperature in cooling_procedure(temp, para):    
        curr_cost = cost(curr_route, cost_matrix)
        new_route = opt2(curr_route, cost_matrix)
        new_cost = cost(new_route, cost_matrix)
        #make decision on whether to move to the new route or not
        p = probability(new_cost, curr_cost, temperature)
        if time.clock() - stime >= cutoff:
            break

        if p == 1:
            curr_route = new_route[:]
            curr_cost = new_cost
            running_time = (time.clock() - stime)
            if curr_cost < best_result:
                best_result = curr_cost
                best_route = curr_route[:]
                trace.append([running_time, curr_cost])
        elif p > random.random():
            curr_route = new_route
            curr_cost = new_cost
        
    return best_result, best_route, trace


