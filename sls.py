import random
import os
import csv
from datetime import datetime

class sls:

    def __init__(self, file):
        self.number_of_item = 0
        self.unvisited = []
        self.adjacency_list = self.read_file(file)
        self.tour = {}
        self.current_tour = []
        self.dist = 0
        
    def generate_random_starting_point(self):
        return random.randint(0, len(self.unvisited)-1)

    def calculate_distance(self, tour):
        dist = 0
        for i in range(len(tour) - 1):
            dist += self.adjacency_list[tour[i]][tour[i+1]]
        
        return dist

    def read_file(self, file):
        f = open(file, "r")
        self.number_of_item = int(f.readline())

        adjacency_list = []

        for i, x in enumerate(f):
            adjacency_list.append([float(dist) for dist in x.split()])
        
        self.unvisited = [i for i in range(self.number_of_item)]
        
        return adjacency_list

    def find_nearest_point(self, current_city, visited):
        
        min_so_far = float("inf")
        closest_city = -1
        distance = self.adjacency_list[current_city]

        for i, j in enumerate(distance):
            if(i!=current_city and j < min_so_far and i not in visited):
                closest_city = i
                min_so_far = j
        
        return closest_city

    def greedy_method(self):
        self.tour = {}
        start_city = self.unvisited[self.generate_random_starting_point()]
        self.unvisited.remove(start_city)
        prev_city = start_city
        current_city = start_city
        visited = []
        while(len(visited) < self.number_of_item):

            visited.append(current_city)
            next_city = self.find_nearest_point(current_city, visited)
            if(next_city != -1):
                current_city = next_city
                prev_city = current_city
            else:
                break

        self.current_tour = visited
        self.current_tour.append(start_city)

    def stochastic_local_search(self):

        iter = 0
        start_time = datetime.now()
        prev_distance = 0
        entropy = 0
        best_dist = float('INF')
        best_tour = []
        while(iter < 1000 and len(self.unvisited) > 0):
            if(entropy < 0.01):
                self.greedy_method()
                prev_distance = self.calculate_distance(self.current_tour)
            for i in range(1,self.number_of_item-1):
                for k in range(i+1, self.number_of_item):
                    new_route = self.current_tour[0:i]
                    sub_route = self.current_tour[i:k+1][::-1]
                    new_route.extend(sub_route)
                    new_route.extend(self.current_tour[k+1:])
                    
                    if(self.calculate_distance(new_route) < self.calculate_distance(self.current_tour)):
                        self.current_tour = new_route    
            iter += 1
            current_dist = self.calculate_distance(self.current_tour)
            entropy = prev_distance - current_dist
            prev_distance = current_dist
            if current_dist < best_dist:
                best_dist = current_dist
                best_tour = self.current_tour

            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= 900:
                print(time_delta.total_seconds())
                break

        #print(best_tour)
        return best_dist

if __name__ == "__main__":

    directory = 'fall20-benchmark-tsp-problems/'
    f = open("result.csv", "w")
    f.write('SLS\n')
    f.write('TSP\n')
    for file in os.listdir(directory):
        if (file != 'readme.md'):
            print('\n'+ file)
            result = ''
            path = directory + file  
            test = sls(path)   
            result = test.stochastic_local_search()
            f.write(file + ', ' + str(result) + '\n')
            