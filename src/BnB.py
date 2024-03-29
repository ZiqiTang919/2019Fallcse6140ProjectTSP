from queue import LifoQueue
import time
import numpy as np

# define a class node to store the attribute of the solution to current point
class Node:
	def __init__(self,n):
		self.visited = [False] * n
		self.start = 1
		self.e = 1
		self.k = 1
		self.sumv = 0
		self.lb = 0
		self.curlist = []
	def __str__(self):
		return 's:' + str(self.start) + "|" + 'e:' + str(self.e) + "|" 'k:' + str(self.k) + "|" + 'cost:' + str(self.sumv) + "|" 'path:' + str(self.curlist)

# define a class Bnb to store the path and cost
class BnB:
	def __init__(self,instance,limit):

		self.dist = instance
		self.INF = 99999999
		self.n = len(self.dist)
		self.pq = LifoQueue()
		self.up = 0
		self.low = 0
		self.isfirst = True

		self.limit = float(limit) #time limit
		if limit == 0:
			self.is_limited = False
		else:
			self.is_limited = True
		self.start_time = time.time()
		self.trace = []

		self.dfs_visited = [False] * self.n
		self.dfs_visited[0] = True
		self.best_solution = self.INF
		self.best_route = [0]


# funciton to calculate the current best cost
	def get_up(self):

		self.up = self.INF

# function to get the lower bound of current branch
	def get_low(self):
		for i in range(self.n):
			temp = self.dist[i]
			self.low = self.low + np.partition(temp, 1)[1] + np.partition(temp, 2)[2]
		self.low = self.low / 2

	def get_lb(self,p):
		remine = p.sumv * 2
		min1 = self.INF
		min2 = self.INF


		for i in range(self.n):
			if p.visited[i] == False and min1 > self.dist[i][p.start]:
				min1 = self.dist[i][p.start]
		remine = remine + min1

		for j in range(self.n):
			if p.visited[j] == False and min2 > self.dist[p.e][j]:
				min2 = self.dist[p.e][j]

		for i in range(self.n):
			if p.visited[i] == False:
				min1 = min2 = self.INF
				for j in range(self.n):
					min1 = self.dist[i][j] if min1 > self.dist[i][j] else min1
				for m in range(self.n):
					min2 = self.dist[i][m] if min2 > self.dist[m][i] else min2
				remine = remine + min1 + min2
		return (remine + 1) / 2

# main function to calculate the best cost and the corresponding trace
# everytime check the lower bound of the current branch
# if the lower bound is worse than the current upper bound, cut the branch
# do not update the upper bound
# if the lower bound is better than the current upper bound, continue this branch and go to the next node
# then update the upper bound to current result
# keep go through all the possible trace and update the upper bound, until all the possible trace are been considered
	def solve(self):
		self.get_up()
		self.get_low()
		node = Node(self.n)
		node.start = 0
		node.e = 0
		node.k = 1
		node.visited = [False] * self.n
		node.curlist.append(0)
		for i in range(self.n):
			node.visited[i] == False
		node.visited[0] = True
		node.sumv = 0
		node.lb = self.low
		remine = self.INF
		optimalsol = self.INF
		self.pq.put(node)
		best_path = None
		while self.pq.qsize() != 0:
			if time.time() - self.start_time > self.limit and self.is_limited == True:
				break
			tmpe = self.pq.get()
			if tmpe.k == self.n - 1: # Is a candidate
				self.isfirst = False
				p = 0
				for i in range(self.n):
					if tmpe.visited[i] == False:
						p = i
						break
				ans = tmpe.sumv + self.dist[tmpe.start][p] + self.dist[p][tmpe.e]
				if ans < optimalsol:
					optimalsol = ans
					printlist = tmpe.curlist
					printlist.append(p)
					# print(str(ans) + str(printlist) + str(time.time() - self.start_time))
					self.trace.append([time.time() - self.start_time,ans])
					best_path = tmpe
					self.best_route = printlist
					self.best_solution = ans

				if ans <= tmpe.lb:
					retmine = min(ans, remine)
					break
				else:
					self.up = min(ans, self.up)
					remine = min(remine, ans)

					continue

			for i in range(self.n):
				if tmpe.visited[i] == False:
					next_node = Node(self.n)
					next_node.start = tmpe.start
					next_node.sumv = tmpe.sumv + self.dist[tmpe.e][i]
					next_node.e = i
					next_node.k = tmpe.k + 1
					next_node.curlist = tmpe.curlist.copy()
					next_node.curlist.append(i)
					next_node.visited = tmpe.visited.copy()
					next_node.visited[i] = True;
					if not self.isfirst:
						next_node.lb = self.get_lb(next_node);
					else:
						next_node.lb = 0
					if not next_node.lb >= self.up:
						self.pq.put(next_node)

		return remine, best_path

#main function to run the code
	def main(self):
		start = time.time()
		sumpath, node = self.solve()
		end = time.time()
		if node is not None:
			list1 = node.curlist.copy()
		else:
			list1 = []

if __name__ == "__main__":
	#instance_list = ['Cincinnati','UKansasState','Berlin','Atlanta','Boston','Champaign','Denver','NYC','Philadelphia','Roanoke','SanFrancisco','Toronto','UMissouri']
	instance_list = ['Cincinnati']
	for item in instance_list:
		print('=========================  Running:' + item)
		test = BnB(item,0)
		test.main()
