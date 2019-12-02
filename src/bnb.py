from queue import LifoQueue
import time
import numpy as np
import src.adjMat as adjMat





class Node:
	def __init__(self,n):
		self.visited = [False] * n
		self.start = 1
		self.e = 1
		self.k = 1
		self.sumv = 0
		self.lb = 0
		self.listc = []
	def __str__(self):
		return 's:' + str(self.start) + "|" + 'e:' + str(self.e) + "|" 'k:' + str(self.k) + "|" + 'cost:' + str(self.sumv) + "|" 'path:' + str(self.listc)

class BnB:
	def __init__(self,instance,limit):

		self.dist = instance
		self.INF = 99999999

		# self.output_solfile_name = 'Output/' + instance + "_BnB_" + str(limit) + ".sol"
		# self.output_tracefile_name = 'Output/' + instance + "_BnB_" + str(limit) + ".trace"

		self.n = len(self.dist)
		# for i in range(self.n):
		# 	self.dist[i][i] = self.INF
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



	def dfs(self,u, k, l):
		if k == self.n - 1:
			return (l + self.dist[u][0])
		minlen = self.INF
		p = 0
		for i in range(self.n):
			if self.dfs_visited[i] == False and minlen > self.dist[u][i]:
				minlen = self.dist[u][i]
				p = i
		self.dfs_visited[p] = True
		return self.dfs(p, k + 1, l + minlen)


	def get_up(self):

		#self.up = self.dfs(0, 0, 0) * 2
		self.up = self.INF


	def get_low(self):
		for i in range(self.n):
			# temp = self.dist[i].copy()
			# temp.sort()
			temp = self.dist[i]
			# print("%s"%(temp[0]))
			self.low = self.low + np.partition(temp, 1)[1] + np.partition(temp, 2)[2]
		self.low = self.low / 2


	def get_lb(self,p):
		ret = p.sumv * 2
		min1 = self.INF
		min2 = self.INF

		for i in range(self.n):
			if p.visited[i] == False and min1 > self.dist[i][p.start]:
				min1 = self.dist[i][p.start]
		ret = ret + min1


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
				ret = ret + min1 + min2
		return (ret + 1) / 2


	def solve(self):
		self.get_up()
		self.get_low()
		node = Node(self.n)
		node.start = 0
		node.e = 0
		node.k = 1
		node.visited = [False] * self.n
		node.listc.append(0)
		for i in range(self.n):
			node.visited[i] == False
		node.visited[0] = True
		node.sumv = 0
		node.lb = self.low
		ret = self.INF
		opt_so_far = self.INF
		self.pq.put(node)
		best_path = None
		while self.pq.qsize() != 0:
			if time.time() - self.start_time > self.limit and self.is_limited == True:
				break
			tmp = self.pq.get()
			#print(str(tmp))
			#print(self.up)
			if tmp.k == self.n - 1: # Is a candidate
				self.isfirst = False
				p = 0
				for i in range(self.n):
					if tmp.visited[i] == False:
						p = i
						break
				ans = tmp.sumv + self.dist[tmp.start][p] + self.dist[p][tmp.e]
				if ans < opt_so_far:
					opt_so_far = ans
					printlist = tmp.listc
					printlist.append(p)
					print(str(ans) + str(printlist) + str(time.time() - self.start_time))
					self.trace.append([time.time() - self.start_time,ans])
					best_path = tmp
					self.best_route = printlist
					self.best_solution = ans



				if ans <= tmp.lb:
					ret = min(ans, ret)
					break
				else:
					self.up = min(ans, self.up)
					ret = min(ret, ans)

					continue


			for i in range(self.n):
				if tmp.visited[i] == False:
					next_node = Node(self.n)
					next_node.start = tmp.start
					next_node.sumv = tmp.sumv + self.dist[tmp.e][i]
					next_node.e = i
					next_node.k = tmp.k + 1
					next_node.listc = tmp.listc.copy()
					next_node.listc.append(i)
					next_node.visited = tmp.visited.copy()
					next_node.visited[i] = True;
					if not self.isfirst:
						next_node.lb = self.get_lb(next_node);
					else:
						next_node.lb = 0
					if not next_node.lb >= self.up:
						self.pq.put(next_node)

		return ret, best_path

	def main(self):

		start = time.time()
		sumpath, node = self.solve()
		end = time.time()
		if node is not None:
			list1 = node.listc.copy()
		else:
			list1 = []

if __name__ == "__main__":
	#instance_list = ['Cincinnati','UKansasState','Berlin','Atlanta','Boston','Champaign','Denver','NYC','Philadelphia','Roanoke','SanFrancisco','Toronto','UMissouri']
	instance_list = ['Cincinnati']
	for item in instance_list:
		print('=========================  Running:' + item)
		test = BnB(item,0)
		test.main()