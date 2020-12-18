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
        self.time_limit = 60  # in seconds , max is 900 (15 min)
        self.output_time_interval = 5
        self.upper_bound = math.inf
        self.result_path = []
        self.pq = PriorityQueue()
        self.start = -1

        # class member for plotting
        self.cost_list = []

    def calc_heuristic(self, target_node, path):
        # for testing
        return 0.0
        return 1.0 / self.adjacency_matrix[path[-1]][target_node]
        min_dist = math.inf
        for i in range(self.num_of_cities):
            if i not in path and self.adjacency_matrix[target_node][i] < min_dist:
                min_dist = self.adjacency_matrix[target_node][i]
        return min_dist

    def bnb_dfs(self):
        # tuple in priority queue (path_length + heuristic, path_length, path)
        #self.pq.put((0.0 - self.calc_heuristic(self.start, [self.start]), 0.0, [self.start]))

        prev_cost = 0.0
        count = 0

        self.pq.put((0.0 - 1, 0.0, [self.start]))
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
                    self.cost_list.append(self.upper_bound)
            else:
                for i in range(self.num_of_cities):
                    if i not in path and path_length + self.adjacency_matrix[tail_of_path][i] < self.upper_bound:
                        #self.pq.put((-self.calc_heuristic(i, path + [i]) - path_length - self.adjacency_matrix[tail_of_path][i], path_length + self.adjacency_matrix[tail_of_path][i], path + [i]))
                        self.pq.put((-1 - len(path) - self.calc_heuristic(i, path), path_length + self.adjacency_matrix[tail_of_path][i], path + [i]))

            if time.time() - time_intermediate >= self.output_time_interval:
                time_intermediate = time.time()
                if self.upper_bound != math.inf:
                    if self.upper_bound == prev_cost:
                        count = count + 1
                    else:
                        count = 0
                    #if count == 6:
                        #return self.result_path, self.upper_bound
                    print(f'Current best: Path={self.result_path}, length={self.upper_bound}\n')
                    #self.cost_list.append(self.upper_bound)
                    prev_cost = self.upper_bound
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

    def calc_dist(self, l):
        dist = 0.0
        for i in range(len(l) - 1):
            dist += self.adjacency_matrix[l[i]][l[i+1]]
        return dist


def draw_diagram_all_in_one(value_list):

    x_list = [[(j + 1) * 5 for j in range(len(value_list[i]))] for i in range(len(value_list))]

    plt.plot(x_list[0], value_list[0], '.-', label='25-62-100-25-1', color='green')
    plt.plot(x_list[1], value_list[1], '.-', label='800-128000-100-25-1', color='purple')
    plt.plot(x_list[2], value_list[2], '.-', label='800-256000-100-5-1', color='mediumvioletred')
    plt.plot(x_list[3], value_list[3], '.-', label='800-256000-100-25-1', color='skyblue')
    plt.legend(loc='best')
    plt.show()


def draw_diagram(value_list):

    # x list is timestamp
    #x_list = [[(j + 1) * 5 for j in range(len(value_list[i]))] for i in range(len(value_list))]

    # x list is count of updates
    x_list = [[(j + 1) for j in range(len(value_list[i]))] for i in range(len(value_list))]

    fig, axs = plt.subplots(2, 2)
    fig.suptitle('Relation between tour cost and run time')

    axs[0, 0].plot(x_list[0], value_list[0], '.-', color='green')
    axs[0, 0].set_title('25-62-100-25-1')
    #axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Tour Cost')

    axs[0, 1].plot(x_list[1], value_list[1], '.-', color='purple')
    axs[0, 1].set_title('75-2250-100-25-1')
    #axs[0, 1].set_xlabel('Time')
    #axs[0, 1].set_ylabel('Tour Cost')

    axs[1, 0].plot(x_list[2], value_list[2], '.-', color='mediumvioletred')
    axs[1, 0].set_title('100-500-100-25-1')
    axs[1, 0].set_xlabel('Time')
    axs[1, 0].set_ylabel('Tour Cost')

    axs[1, 1].plot(x_list[3], value_list[3], '.-', color='skyblue')
    axs[1, 1].set_title('200-4000-100-5-1')
    axs[1, 1].set_xlabel('Time')
    #axs[1, 1].set_ylabel('Tour Cost')

    plt.show()


def draw():
    value_list = []  # for plotting
    path_list = []
    cost_list = []  # for output

    f_list = ['tsp-problem-25-62-100-25-1.txt', 'tsp-problem-75-2250-100-25-1.txt', 'tsp-problem-100-500-100-25-1.txt', 'tsp-problem-200-4000-100-5-1.txt']

    for f in f_list:
        tsp = TSP(f)
        tsp.test_once()
        value_list.append(tsp.cost_list)
        path_list.append(tsp.result_path)
        cost_list.append(tsp.upper_bound)

    draw_diagram_all_in_one(value_list)
    draw_diagram(value_list)

    print(f'Path={path_list[0]}, Length={cost_list[0]}')
    print(f'Path={path_list[1]}, Length={cost_list[1]}')
    print(f'Path={path_list[2]}, Length={cost_list[2]}')
    print(f'Path={path_list[3]}, Length={cost_list[3]}')


if __name__ == '__main__':

    # uncomment this to run test in 4 test problems and draw diagram
    #draw()

    file_name = 'tsp-problem-25-62-100-25-1.txt'
    tsp = TSP(file_name)
    tsp.test_once()
