import random 
import matplotlib.pyplot as plt

class Location(object):
    def __init__(self,x,y):
        '''x and y are floats'''
        self.x = x 
        self.y = y 
        
    def move(self, delta_x, delta_y):
        '''delta_x and delta_y are floats'''
        return Location(self.x + delta_x, self.y + delta_y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y 
    
    def distFrom(self,other):
        ox = other.x
        oy = other.y
        x_dist = self.x - ox 
        y_dist = self.y - oy
        return (x_dist**2 + y_dist**2)**0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'
    
class Field(object):
    def __init__(self):
        self.drunks = {}
        
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate Drunk')
        else:
            self.drunks[drunk] = loc
    
    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in Field')
        xDist, yDist = drunk.take_step()
        current_location = self.drunks[drunk]
        #use move method of Location to get new Location
        self.drunks[drunk] = current_location.move(xDist, yDist)
        
    def get_loc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in Field')
        return self.drunks[drunk]

class Drunk(object):
    def __init__(self, name=None):
        '''assumes name is a str'''
        self.name = name 
    
    def __str__(self,):
        if self != None:
            return self.name 
        return 'Anonymous'
    
class UsualDrunk(Drunk):
    def take_step(self):
        step_choices = [(0,1),(1,0), (0,-1), (-1,0)]
        return random.choice(step_choices)
    
def walk(f, d, num_steps):
    '''
    Assumes: f a Field, d a Drunk in f, and num_steps an int >= 0
    Moves d num_steps times and returns the difference between 
    the final location and the location at the start of the walk
    '''
    start = f.get_loc(d)
    for s in range(num_steps):
        f.moveDrunk(d)
    return start.distFrom(f.get_loc(d))

def sim_walks(num_steps, num_trials, dClass):
    '''
    Assumes num_steps an int >= 0, num_trials an int >= 0
        dClass a subclass of drunk
    Simulates num_trials walks of num_steps steps each
    Returns a list of the final distances for each trial
    '''
    Homer = dClass()
    origin = Location(0,0)
    distances = []
    for t in range(num_trials):
        f = Field() 
        f.addDrunk(Homer, origin)
        distances.append(walk(f, Homer, num_steps))
    return distances 

def stdDev(x):
    '''
    Assumes that x is a list of numbers.
    Returns the Standard Deviation of x
    '''
    mean = sum(x)/len(x)
    tot = 0 
    for i in x:
        tot += (i - mean)**2
    return (tot/len(x))**0.5

def CV(x):
    mean = sum(x) /len(x)
    try:
        return stdDev(x)/mean 
    except ZeroDivisionError:
        return float('nan')

def drunk_test(walk_lengths, num_trials, dClass):
    '''
    Assumes walk_lengths a sequence of ints >=0
        num_trials an int > 0, dClass a subclass of Drunk
    For each number of steps in walk_lengths, runs sim_walks with
        num_trials walks and prints results
    '''
    for num_steps in walk_lengths:
        distances = sim_walks(num_steps, num_trials, dClass)
        print(dClass.__name__, 'random walk of', num_steps,'steps')
        print('Mean =', sum(distances)/len(distances), \
            'CV =', CV(distances))
        print('Max =', max(distances), 'Min =', min(distances))
        
        
class ColdDrunk(Drunk):
    def take_step(self):
        step_choices = [(0,1), (0,-2), (1,0),(-1,0)]
        return random.choice(step_choices)
    
class EWDrunk(Drunk):
    def take_step(self):
        step_choices = [(1,0), (-1,0)]
        return random.choice(step_choices)
        
class StyleIterator(object):
    def __init__(self, styles):
        self.index = 0 
        self.styles = styles 
        
    def next_style(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0 
        else:
            self.index += 1
        return result 
    
def sim_drunk(num_trials, dClass, walk_lengths):
    mean_distances = []
    cv_distances = []
    for num_steps in walk_lengths:
        print('Starting simulation of',num_steps, 'steps')
        trials = sim_walks(num_steps, num_trials, dClass)
        mean = sum(trials)/len(trials)
        mean_distances.append(mean)
        cv_distances.append(stdDev(trials)/ mean)
    return (mean_distances, cv_distances)

def sim_all(drunk_kinds, walk_lengths, num_trials):
    style_choice = StyleIterator(('b-','r:','m-.'))
    for dClass in drunk_kinds:
        cur_style = style_choice.next_style()
        print('Starting simulation of',dClass.__name__)
        means, cvs = sim_drunk(num_trials, dClass, walk_lengths)
        cv_mean = sum(cvs)/len(cvs)
        plt.plot(walk_lengths, means, cur_style,
                 label=dClass.__name__+'(CV = '+str(round(cv_mean, 4))+')')
    plt.title('Mean Distance from Origin (' + str(num_trials) + ' trials)')
    plt.xlabel('Number of Steps')
    plt.ylabel('Distance from Origin')
    plt.legend(loc='best')
    plt.semilogx()
    plt.semilogy()
        
# sim_all((UsualDrunk,ColdDrunk,EWDrunk), (10,100,1000,10000,100000),100)

def get_final_locs(num_steps, num_trials, dClass):
    locs = []
    d = dClass()
    origin = Location(0,0)
    for t in range(num_trials):
        f = Field() 
        f.addDrunk(d, origin)
        for s in range(num_steps):
            f.moveDrunk(d)
        locs.append(f.get_loc(d))
    return locs 

def plot_locs(drunk_kinds, num_steps, num_trials):
    style_choice = StyleIterator(('b+','r^','mo'))
    for dClass in drunk_kinds:
        locs = get_final_locs(num_steps, num_trials, dClass)
        x_vals, y_vals = [],[]
        for l in locs:
            x_vals.append(l.get_x())
            y_vals.append(l.get_y())
        mean_x = sum(x_vals)/len(x_vals)
        mean_y = sum(y_vals)/len(y_vals)
        cur_style = style_choice.next_style()
        plt.plot(x_vals, y_vals, cur_style, 
                 label=dClass.__name__ + 'Mean loc. = <'
                 +str(mean_x) + ', ' + str(mean_y) + '>')
    plt.title('Location at End of Walks ('
              + str(num_steps) + ' steps')
    plt.xlabel('Steps East/West of Origin')
    plt.ylabel('Steps North/South of Origin')
    plt.legend(loc='lower left', numpoints = 1)
    
plot_locs((UsualDrunk,ColdDrunk,EWDrunk),1000,2000)


class OddField(Field):
    def __init__(self, num_holes=1000, x_range=100, y_range=100):
        Field.__init__(self)
        self.worm_holes = {}
        for w in range(num_holes):
            x = random.randint(-x_range,x_range)
            y = random.randint(-y_range,y_range)
            new_x = random.randint(-x_range,x_range)
            new_y = random.randint(-y_range,y_range)
            new_loc = Location(new_x,new_y)
            self.worm_holes[(x,y)] = new_loc
            
    def moveDrunk(self, drunk):
        Field.moveDrunk(self,drunk)
        x = self.drunks[drunk].get_x()
        y = self.drunks[drunk].get_y() 
        if (x,y) in self.worm_holes:
            self.drunks[drunk] = self.worm_holes[(x,y)]


def trace_walk(field_kinds, num_steps):
    style_choice = StyleIterator(('b+','r^','ko'))
    for fClass in field_kinds:
        d = UsualDrunk()
        f = fClass()
        f.addDrunk(d, Location(0,0))
        locs = []
        for s in range(num_steps):
            f.moveDrunk(d)
            locs.append(f.get_loc(d))
        x_vals = []
        y_vals = []
        for l in locs:
            x_vals.append(l.get_x())
            y_vals.append(l.get_y())
        cur_style = style_choice.next_style()
        plt.plot(x_vals, y_vals, cur_style,
                 label=fClass.__name__)
    plt.title('Spots Visited on Walk ('
              + str(num_steps) + ' steps)')
    plt.xlabel('Steps East/West of Origin')
    plt.ylabel('Steps North/South of Origin')
    plt.legend(loc='best')
    
trace_walk((Field, OddField),500)
