from Knapsack import Item 
import random

def fastFib(n, memo={}):
    '''
    Assumes n is an int >= 0, memo used only by recursive calls
    Returns Fibonacci of n
    '''
    if n <= 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fastFib(n-1, memo) + fastFib(n-2, memo)
        memo[n] = result
        return result
    
def max_val(to_consider, avail):
    '''
    Assumes to_consider a list of items, avail a weight
    Returns a tuple of the total value of a solution to 0/1 knapsack
        problem and the items of that solution
    '''
    if to_consider == [] or avail == 0:
        result = (0,())
    elif to_consider[0].get_weight() > avail:
        # Explore the right branch only
        result = max_val(to_consider[1:], avail)
    else:
        next_item = to_consider[0]
        # Explore left branch
        with_val, with_to_take = max_val(to_consider[1:], avail - next_item.get_weight())
        with_val += next_item.get_value()
        # Explore right branch
        without_val, without_to_take = max_val(to_consider[1:], avail)
        # Choose better Branch 
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    return result 


def small_test():
    names = ['a','b','c','d']
    vals = [6,7,8,9]
    weights = [2,2,3,5]
    Items = []
    for i in range(len(vals)):
        Items.append(Item(names[i], vals[i], weights[i]))
    val, taken = max_val(Items, 5)
    for item in taken:
        print(item)
    print('Total value of items taken =', val)
    
# small_test()

def build_many_items(num_items, max_val, max_weight):
    items = []
    for i in range(num_items):
        items.append(Item(str(i), random.randint(1,max_val)
                          , random.randint(1,max_weight)))
    return items

def big_test(num_items):
    items = build_many_items(num_items, 10,10)
    val, taken = max_val(items,40)
    print('Items Taken')
    for item in taken:
        print(item)
        print('Total Value of the items taken =', val)
        
def fast_max_val(to_consider, avail, memo={}):
    '''
    Assumes to_consider a list of items, avail a weight
        memo used only by recursive calls
    Returns a tuple of the total weight of a solution to the
        0/1 knapsack problem and the items of that solution
    '''
    if (len(to_consider), avail) in memo:
        result = memo[(len(to_consider), avail)]
    elif to_consider == [] or avail == 0:
        result = (0,())
    elif to_consider[0].get_weight() > avail:
        # Explore the right branch only
        result = fast_max_val(to_consider[1:], avail, memo)
    else:
        next_item = to_consider[0]
        # Explore the left branch
        with_val, with_to_take = fast_max_val(to_consider[1:],
                                            avail - next_item.get_weight(),
                                            memo)
        with_val += next_item.get_value()
        # Explore Right branch
        without_val, without_to_take = fast_max_val(to_consider[1:],
                                                    avail,
                                                    memo)
        # Choose better branch
        if with_val > without_val:
            result = (with_val, with_to_take + (next_item,))
        else:
            result = (without_val, without_to_take)
    memo[(len(to_consider), avail)] = result
    return result 
    