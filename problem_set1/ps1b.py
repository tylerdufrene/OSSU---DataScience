###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

import random

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    print(egg_weights, target_weight)
    if (len(egg_weights), target_weight) in memo:
        result = memo[(len(egg_weights), target_weight)]
    elif egg_weights == () or target_weight == 0:
        result = 0
    elif egg_weights[-1] > target_weight:
        result = dp_make_weight(egg_weights[:-1], target_weight, memo)
    else:
        next_item = egg_weights[-1]
        with_egg = dp_make_weight(egg_weights[:], 
                                            target_weight - next_item,
                                            memo)
        with_egg += 1
        result = with_egg
    memo[(len(egg_weights), target_weight)] = result
    # print(memo)
    return result

def buildRandomEggTuple(numItems, maxWeight):
    egg_weights = []
    for i in range(numItems):
        egg_weights.append(random.randint(1, maxWeight))
    return tuple(sorted(egg_weights))

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    egg_weights = (1, 5, 10, 20)
    n = 99
    print("Egg weights = (1, 5, 10, 20)")
    print("n = 99")
    print("Expected ouput: 10 (4 * 20 + 1 * 10 + 1 * 5 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    egg_weights = buildRandomEggTuple(50, 90)
    n = 99
    print("Egg weights =", egg_weights)
    print("n = 99")
    #print("Expected ouput: 10 (4 * 20 + 1 * 10 + 1 * 5 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    

    
    
'''
WRITE-UP
1. Explain why it would be difficult to use a brute force algorithm to solve this problem   
    if there were 30 different egg weights. 
    - It would be difficult to solve this problem with the given prompt because brute force
        requires an enumeration of all possible weight combinations. 30 Weights would generate
        a partition list of length 1,073,741,824. In order to test all of these weight combinations
        it would take quite a while
--------------------------
2. If you were to implement a greedy algorithm for finding the minimum number of eggs 
    needed, what would the objective function be? What would the constraints be? What strategy 
    would your greedy algorithm follow to pick which coins to take?
    - The objective function would be the minimum number of eggs. This is the value that we want to 
        minimize. The constraints would be the total available weight remaining on the ship. The strategy
        would be: remove from the target weight, the largest set of weights until that weight is larger than
        the remaining target weight. Then move down to smaller weights until you have target_weight remaining
----------------------------
3. Will a greedy algorithm always return the optimal solution to this problem? Explain why it is 
    optimal or give an example of when it will not return the optimal solution.
    - As long as the Egg weights are ordered in descending order and there is sufficient weight size
        to satisfy the remaining target weight, the optimal solution should always be found.
'''