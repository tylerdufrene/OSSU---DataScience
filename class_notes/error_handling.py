def isPal(x):
    '''
    Assumes x is a list
    Returns True if the list is a palindrom; false otherwise
    '''
    temp = x 
    temp.reverse()
    if temp == x:
        return True 
    else:
        return False 
    
def silly(n):
    '''
    Assumes n is an int > 0
    Gets n inputs from user
    Prints 'Yes' if the sequence of inputs forms a palindrome; 'No' Otherwise
    '''
    result = []
    for i in range(n):
        elem = input('Enter element: ')
        result.append(elem)
    if isPal(result):
        print('Yes')
    else:
        print('No')
        
        
def sumDigits(s):
    '''
    Assumes s is a string
    Returns the sum of the decimal digits in s
        For example if s is a2b3c it returns 5
    '''
    total = 0
    for item in s:
        try:
            total += int(item)
        except: 
            print(item, 'is not a number')
    return total 

def readVal(valType, request_msg, error_msg):
    while True:
        val = input(request_msg+ ' ')
        try:
            val = valType(val)
            print('The square of the number you entered is', val**2)
            break 
        except ValueError:
            print(val,'is not an integer')

def findAnEven(l):
    '''
    Assumes l is a list of integers
    Returns the first even number in l
    Raises ValueError if l does not contain an even Number
    '''
    evens = [item for item in l if item % 2 == 0]
    if len(evens) == 0:
        raise ValueError('No even numbers in l')
    return evens[0]
    