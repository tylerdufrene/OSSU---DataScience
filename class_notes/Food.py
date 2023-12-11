class Food(object):
    def __init__(self, n, v, w):
        self.name = n 
        self.value = v
        self.calories = w 
        
    def getValue(self):
        return self.value
    
    def getCost(self):
        return self.calories
    
    def density(self):
        return self.getValue()/self.getCost()
    
    def __str__(self):
        return self.name + ': <' + str(self.value) + ', ' + str(self.calories) + '>'
    
def buildMenu(names, values, calories):
    '''
    names, values, calories lists of same length.
    name a list of strings 
    values and calories lists of numbers
    returns a list of foods
    '''
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i], calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    '''
    Assumes items a list, maxCost >= 0,
    keyfunction maps elemtns of items to numbers'''
    itemsCopy = sorted(items, key=keyFunction,reverse=True)
    result = []
    totalValue, totalCost = 0,0
    
    for i in range(len(itemsCopy)):
        if (totalCost + itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

def testGreedy(items, constraint, keyfunction):
    taken, val = greedy(items, constraint, keyFunction=keyfunction)
    print('Total Value of Items Taken =', val)
    for item in taken:
        print(' ', item)
        
def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, lambda x: 1/Food.getCost(x))
    print('\nUser greedy by density to allocate',maxUnits,'calories')
    testGreedy(foods, maxUnits, Food.density)

names = ['wine','beer','pizza','burger','fries','cola','apple','donut','cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]
foods = buildMenu(names, values, calories)


def max_val(to_consider, avail):
    '''
    Assumes to_consider a list of items, avail a weight
    Returns a tuple of the total value of a solution to 0/1 knapsack
        problem and the items of that solution
    '''
    if to_consider == [] or avail == 0:
        result = (0,())
    elif to_consider[0].getCost() > avail:
        # Explore the right branch only
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        # Explore left branch
        with_val, with_to_take = max_val(to_consider[1:], avail - next_item.getCost())
        with_val += next_item.getValue()
        # Explore right branch
        without_val, without_to_take = max_val(to_consider[1:], avail)
        # Choose better Branch 
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result 

def max_val_fast(to_consider, avail, memo={}):
    '''
    Assumes to_consider a list of items, avail a weight
    Returns a tuple of the total value of a solution to 0/1 knapsack
        problem and the items of that solution
    '''
    if to_consider == [] or avail == 0:
        result = (0,())
    elif to_consider[0].getCost() > avail:
        # Explore the right branch only
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        # Explore left branch
        with_val, with_to_take = max_val(to_consider[1:], avail - next_item.getCost())
        with_val += next_item.getValue()
        # Explore right branch
        without_val, without_to_take = max_val(to_consider[1:], avail)
        # Choose better Branch 
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result 


def test_max_val(foods, max_units, print_items = True):
    print('Use search tree to allocate', max_units, 'calories')
    val, taken = max_val(foods, max_units)
    print('Total value of items taken =', val)
    if print_items:
        for item in taken:
            print(' ', item)
            
# testGreedys(foods, 750)
# print('')
# test_max_val(foods, 750)

import random 

def build_large_menu(num_items, max_val, max_cost):
    items = []
    for i in range(num_items):
        items.append(Food(str(i), random.randint(1,max_val)
                     , random.randint(1,max_cost)))
    return items 

# for num_items in (5,10,15,20,25,30,35,40,45,50,55,60):
#     print('Try a menu with',num_items,'items')
#     items = build_large_menu(num_items,90,250)
#     test_max_val(items, 750, False)
        
        
def fib(n):
    if n == 0 or n== 1:
        return 1 
    else:
        return fib(n-1) + fib(n-2)
    
def fast_fib(n, memo={}):
    ''' 
    Assumes n is an int >= 0, memo used only by recursion
    Returns Fibonacci of n
    '''
    if n == 0 or n == 1:
        return 1 
    try:
        return memo[n]
    except KeyError:
        result = fast_fib(n-1,memo) + fast_fib(n-2, memo)
        memo[n] = result 
        return result 

for i in range(121):
    print('fib(' + str(i) + ') =', fast_fib(i))