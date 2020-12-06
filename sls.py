import random

class sls:

    def __init__(self, file):
        self.number_of_item = 0
        self.adjacency_list = self.read_file(file)
        self.current_tour = []
        self.dist = 0
        self.greedy_method()
        
    def generate_random_starting_point(self):
        return random.randint(0, self.number_of_item-1)

    def calculate_distance(self):
        for edge in self.current_tour:
            self.dist += self.adjacency_list[edge[0]][edge[1]]
    
    def print_result(self):
        print("current tour distance " + str(self.dist))
        print(self.current_tour)

    def read_file(self, file):
        f = open(file, "r")
        self.number_of_item = int(f.readline())

        adjacency_list = []

        for i, x in enumerate(f):
            adjacency_list.append([float(dist) for dist in x.split()])
        
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
        
        start_city = self.generate_random_starting_point()
        current_city = start_city
        visited = []
        while(len(self.current_tour) != self.number_of_item-1):
            visited.append(current_city)
            next_city = self.find_nearest_point(current_city, visited)
            if(next_city != -1):
                self.current_tour.append((current_city,next_city))
                current_city = next_city
            else:
                break
        self.current_tour.append((current_city, start_city))
        self.calculate_distance()
    
    def stochastic_local_search(self):
        pass


if __name__ == "__main__":
    test = sls("tsp-problem-3-3-1-2-1.txt")
    test.print_result()