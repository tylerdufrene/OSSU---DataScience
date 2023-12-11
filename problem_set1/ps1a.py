###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import numpy as np 

#================================
# Part A: Transporting Space Cows
#================================

class Cow:
    def __init__(self,name,weight):
        self.name = name 
        self.weight = weight 
    def get_name(self):
        return self.name
    def get_weight(self):
        return self.weight
    def __str__(self):
        return '<' + self.name + ', ' + str(self.weight) + '>'
    


# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cow_file = open(filename).readlines()
    cow_dict = {}
    for cow in cow_file:
        name_weight = cow.split(',')
        try:
            cow_dict[name_weight[0]] = int(name_weight[1].replace('\n',''))
        except ValueError:
            pass
    return cow_dict      

def get_biggest_cow(cow_dict):
    largest_cow,name = 0,''
    for c,w in cow_dict.items():
        if w > largest_cow:
            largest_cow,name = w,c 
    return (name, largest_cow)

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = cows.copy()
    transport_list = []
    transport = 0
    while cows_copy:
        total_weight = 0
        limit_reached=False
        transport += 1
        single_transport = []
        while total_weight <= limit and not limit_reached:
            temp_cows = {c:w for c,w in cows_copy.items() if w + total_weight <= limit}
            if temp_cows:
                cow = get_biggest_cow(temp_cows)
                cows_copy.pop(cow[0])
                single_transport.append(cow[0])
                total_weight += cow[1]
                # print(cow[0], 'added to transport')
            else:
                transport_list.append(single_transport)
                # print('Limit Reached. Closing transport')
                limit_reached = True 
    return transport_list
            
        

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    power_set = get_partitions(cows)
    best_set, transport_count = None, np.inf
    for cow_set in power_set:
        # print('-----')
        # print('Cow_set =',cow_set)
        transport_weight = []
        for cow in cow_set:
            part = sum([cows[c] for c in cow])
            transport_weight.append(part)
        # print('Weight of Transports =',transport_weight)
        partition_works = any([w for w in transport_weight if w > limit])
        if partition_works:
            # print('Fails transport weight constraint')
            continue
        else:
            if len(cow_set) < transport_count:
                # print('New Best Set:',cow_set)
                best_set = cow_set
                transport_count = len(cow_set)
    return best_set

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows('ps1_cow_data.txt')
    greedy_start = time.time()
    greedy = greedy_cow_transport(cows)
    greedy_end = time.time()
    print('Greedy Algorithm found a transport of length',str(len(greedy)),
          'in',str(greedy_end-greedy_start))
    print('-'*10)
    brute_force_start = time.time()
    bf = brute_force_cow_transport(cows)
    brute_force_end = time.time()
    print('Brute-Force Algorithm found a transport of length',str(len(bf)),
            'in',str(brute_force_end-brute_force_start))
    
compare_cow_transport_algorithms()
'''
Greedy Algorithm found a transport of length 6 in 0.0
----------
Brute-Force Algorithm found a transport of length 5 in 0.9184422492980957

Greedy Algorithm is quicker to run but does not find the optimal solution.
BF algorithm finds the optimal solution but takes longer to run
'''