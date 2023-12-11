class Item(object):
    def __init__(self, n,v,w):
        self.name = n
        self.value = v 
        self.weight = w 
    def get_name(self):
        return self.name 
    def get_value(self):
        return self.value
    def get_weight(self):
        return self.weight 
    def __str__(self):
        result = '<' + self.name + ', ' + str(self.value) \
            + ', ' + str(self.weight) + '>'
        return result 
    
def value(item):
    return item.get_value()

def weight_inverse(item):
    return 1/ item.get_weight()

def density(item):
    return item.get_value() / item.get_weight()

def build_items():
    names = ['clock','painting','radio','vase','book','computer']
    values = [175,90,20,50,10,200]
    weights = [10,9,4,2,1,20]
    items = []
    for i in range(len(values)):
        items.append(Item(names[i], values[i], weights[i]))
    return items 

def greedy(items, max_weight, key_function):
    '''
    Assumes Items a list, max_weight >= 0, 
        key_function maps elements of Items to floats
    '''
    items_copy = sorted(items, key=key_function, reverse=True)
    result = []
    total_value = 0
    total_weight = 0 
    for i in range(len(items_copy)):
        if (total_weight + items_copy[i].get_weight()) <= max_weight:
            result.append(items_copy[i])
            total_weight += items_copy[i].get_weight()
            total_value += items_copy[i].get_value()
    return (result, total_value)

def test_greedy(items, constraint, key_function):
    taken, val = greedy(items, constraint, key_function)
    print('Total valu of items taken =',val)
    for item in taken:
        print(' ', item)
        
def test_greedies(max_weight = 20):
    items = build_items()
    print('Use greedy by value to fill knapsack of size', max_weight)
    test_greedy(items, max_weight, value)
    print('\nUse Greedy by weight to fill knapsack of size',max_weight)
    test_greedy(items, max_weight, weight_inverse)
    print('\nUse greedy by density to fill knapsack of size', max_weight)
    test_greedy(items, max_weight, density)
    
def choose_best(pset, max_weight, get_val, get_weight):
    best_val = 0
    best_set = None
    for items in pset:
        items_val = 0 
        items_weight = 0
        for item in items:
            items_val += get_val(item) 
            items_weight += get_weight(item)
        if items_weight <= max_weight and items_val > best_val:
            best_val = items_val
            best_set = items 
    return (best_set, best_val)

def get_binary_rep(n, num_digits):
    '''
    Assumes n and num_digits are non-negative ints 
    Returns a num_digits str that is a binary representation 
        of n 
    '''
    result = ''
    while n > 0:
        result = str(n%2) + result 
        n = n//2
    if len(result) > num_digits:
        raise ValueError('not enough digits')
    for i in range(num_digits - len(result)):
        result = '0' + result 
    return result 

def gen_power_set(L):
    '''
    Assumes L is a list
    Returns a list of lists taht contains all possible combinations
        of the element L
    '''
    power_set = []
    for i in range(0, 2**len(L)):
        bin_str = get_binary_rep(i, len(L))
        subset = []
        for j in range(len(L)):
            if bin_str[j] == '1':
                subset.append(L[j])
        power_set.append(subset)
    return power_set
    
def test_best(max_weight = 20):
    items = build_items()
    pset = gen_power_set(items)
    taken, val = choose_best(pset, max_weight, Item.get_value, Item.get_weight)
    print('Total value of items taken =', val)
    for item in taken:
        print(item)