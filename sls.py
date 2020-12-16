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

    def calculate_distance(self):
        self.dist = 0
        for start, end in self.tour.items():
            self.dist += self.adjacency_list[start][end]

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
        
        start_city = self.unvisited[self.generate_random_starting_point()]
        self.unvisited.remove(start_city)
        current_city = start_city
        visited = []
        while(len(visited) < self.number_of_item):
            visited.append(current_city)
            next_city = self.find_nearest_point(current_city, visited)
            if(next_city != -1):
                self.tour[current_city] = next_city
                current_city = next_city
            else:
                break

        self.tour[current_city] = start_city
        self.current_tour = visited
        self.calculate_distance()
    
    def look_up_start_city(self, dest_city):
        for start in self.tour:
            if self.tour[start] == dest_city:
                return start
        return ''

    def compare_distance(self, old_route, new_route):
        old_dist = new_dist = 0
        for edge in old_route:
            old_dist += self.adjacency_list[edge[0]][edge[1]]
        for edge in new_route:
            new_dist += self.adjacency_list[edge[0]][edge[1]]
        
        return new_dist < old_dist

    def stochastic_local_search(self):

        iter = 0
        start_time = datetime.now()
        prev_distance = self.dist
        entropy = 0
        best_dist = float('INF')
        while(iter < 1000 and len(self.unvisited) > 0):
            if(entropy < 0.01):
                self.greedy_method()
            for city_a in range(self.number_of_item-1):
                for city_c in range(city_a+1, self.number_of_item):
                    city_b = self.tour[city_a]
                    city_d = self.tour[city_c]
                    if(city_d == city_a or city_c == city_b):
                        continue
                    shorter = self.compare_distance([(city_a, city_b), (city_c, city_d)], [(city_a, city_d), [city_c, city_b]])
                    if(shorter):
                        self.tour[city_a] = city_d
                        self.tour[city_c] = city_b
            iter += 1
            self.calculate_distance()
            entropy = prev_distance - self.dist
            prev_distance = self.dist
            if self.dist < best_dist:
                best_dist = self.dist

            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= 900:
                break
        
        self.dist = best_dist

if __name__ == "__main__":

    directory = ('fall20-benchmark-tsp-problems/')
    path = ''
    
    index = 0
    
    f = open("result1.csv", "w")
    f.write('SLS\n')
    f.write('TSP\n')
    for file in os.listdir(directory):
        if (file != 'readme.md'):
            print('\n'+ file)
            result = ''
            path = directory + file  
            test = sls(path)   
            test.stochastic_local_search()
            f.write(str(test.dist) + '\n')
            index += 1





    '''    
    def stochastic_local_search(self):

        iter = 0
        while(iter < 1000):
            current_city = self.generate_random_starting_point()
            index = self.current_tour.index(current_city)
            indexs = self.calculate_index(index)
            add_edge = list(filter(lambda x: x != current_city and x!= self.current_tour[indexs[0]] and x!= self.current_tour[indexs[1]], self.current_tour))
            print(add_edge)
            break


    def stochastic_local_search(self):
        iter = 0
        self.greedy_method()
        prev_distance = self.dist
        entropy = 1

        while(iter < 1000):
            city_a = self.generate_random_starting_point()
            unvisited = list(filter(lambda x: x!=city_a, self.tour.keys()))
            for city_c in unvisited:
                city_b = self.tour[city_a]
                city_d = self.tour[city_c]
                if(city_d == city_a or city_c == city_b):
                    continue
                shorter = self.compare_distance([(city_a, city_b), (city_c, city_d)], [(city_a, city_d), [city_c, city_b]])
                if(shorter):
                    self.tour[city_a] = city_d
                    self.tour[city_c] = city_b
            iter += 1
            self.calculate_distance()
            entropy = prev_distance - self.dist
            prev_distance = self.dist
'''