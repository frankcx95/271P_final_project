import numpy as np
import matplotlib.pyplot as plt
import math
import time
from random import randrange
from queue import PriorityQueue

class TSP:

    def __init__(self, problem_file_name):

        # initialize adjacency matrix
        file = open(problem_file_name, 'r')
        self.num_of_cities = int(file.readline())
        self.adjacency_matrix = []
        for _ in range(self.num_of_cities):
            tmp_list = file.readline().split(' ')
            self.adjacency_matrix.append([float(elem) for elem in tmp_list])

        # initialize class members
        self.time_limit = 900  # in seconds , max is 900 (15 min)
        self.output_time_interval = 10
        self.upper_bound = math.inf
        self.result_path = []
        self.pq = PriorityQueue()
        self.start = -1

        # class member for plotting
        self.cost_list = []


    def calc_heuristic(self, target_node, path):
        return 0.0
        min_dist = math.inf
        for i in range(self.num_of_cities):
            if i not in path and self.adjacency_matrix[target_node][i] < min_dist:
                min_dist = self.adjacency_matrix[target_node][i]
        return min_dist

    def bnb_dfs(self):
        # tuple in priority queue (path_length + heuristic, path_length, path)
        self.pq.put((0.0 - self.calc_heuristic(self.start, [self.start]), 0.0, [self.start]))
        time_start = time.time()
        time_intermediate = time_start
        while not self.pq.empty() and time.time() - time_start < self.time_limit:
            curr = self.pq.get()
            priority, path_length, path = curr
            tail_of_path = path[-1]
            if len(path) == self.num_of_cities:
                if path_length + self.adjacency_matrix[tail_of_path][self.start] < self.upper_bound:
                    path.append(self.start)
                    self.result_path = path
                    self.upper_bound = path_length + self.adjacency_matrix[tail_of_path][self.start]
            else:
                for i in range(self.num_of_cities):
                    if i not in path and path_length + self.adjacency_matrix[tail_of_path][i] < self.upper_bound:
                        self.pq.put((-self.calc_heuristic(i, path + [i]) - path_length - self.adjacency_matrix[tail_of_path][i], path_length + self.adjacency_matrix[tail_of_path][i], path + [i]))

            if time.time() - time_intermediate >= self.output_time_interval:
                time_intermediate = time.time()
                print(f'Path={self.result_path}, length={self.upper_bound}\n')
                if self.upper_bound != math.inf:
                    self.cost_list.append(self.upper_bound)

        return self.result_path, self.upper_bound

    # run tsp solver, if the start node is not specified, a random node will be chosen
    def test_once(self, start=-1):
        if start == -1:
            self.start = randrange(self.num_of_cities)
        else:
            self.start = start
        print(f'Starting from node {self.start}:')
        self.bnb_dfs()
        print(f'[FINAL] Path={self.result_path}, length={self.upper_bound}\n')

    # run tsp solver multiple times starting from each node, used for checking correctness in trivial cases
    def test_start_from_each_node(self):
        for i in range(self.num_of_cities):
            self.test_once(i)
            self.reset()

    # reset the tsp solver to initial state
    def reset(self):
        self.upper_bound = math.inf
        self.result_path = []
        self.pq = PriorityQueue()

def draw_diagram(value_list):

    x_list = [[(j + 1) * 10 for j in range(len(value_list[i]))] for i in range(len(value_list))]

    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Relation between tour cost and run time')

    axs[0, 0].plot(x_list[0], value_list[0], 'o-')
    axs[0, 0].set_title('25-62-100-25-1')
    #axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Tour Cost')

    axs[0, 1].plot(x_list[1], value_list[1], 'o-')
    axs[0, 1].set_title('75-2250-100-25-1')
    #axs[0, 1].set_xlabel('Time')
    #axs[0, 1].set_ylabel('Tour Cost')

    axs[1, 0].plot(x_list[2], value_list[2], 'o-')
    axs[1, 0].set_title('100-500-100-25-1')
    axs[1, 0].set_xlabel('Time')
    axs[1, 0].set_ylabel('Tour Cost')

    axs[1, 1].plot(x_list[3], value_list[3], 'o-')
    axs[1, 1].set_title('200-4000-100-5-1')
    axs[1, 1].set_xlabel('Time')
    #axs[1, 1].set_ylabel('Tour Cost')

    plt.show()

if __name__ == '__main__':

    value_list = []

    f1 = 'tsp-problem-25-62-100-25-1.txt'
    tsp = TSP(f1)
    tsp.test_once(start=0)
    value_list.append(tsp.cost_list)

    f2 = 'tsp-problem-75-2250-100-25-1.txt'
    tsp = TSP(f2)
    tsp.test_once(start=0)
    value_list.append(tsp.cost_list)

    f3 = 'tsp-problem-100-500-100-25-1.txt'
    tsp = TSP(f3)
    tsp.test_once(start=0)
    value_list.append(tsp.cost_list)

    f4 = 'tsp-problem-200-4000-100-5-1.txt'
    tsp = TSP(f4)
    tsp.test_once(start=0)
    value_list.append(tsp.cost_list)

    draw_diagram(value_list)
