import random
import matplotlib.pyplot as plt
import numpy as np
from math import factorial

def roll_die():
    return random.choice([1,2,3,4,5,6]) # Uniform distribution

def test_roll(n=10):
    result = ''
    for i in range(n):
        result += str(roll_die())
    return result

def run_sim(goal, num_trials, txt):
    total = 0
    for i in range(num_trials):
        result = ''
        for j in range(len(goal)):
            result += str(roll_die())
        if result == goal:
            total += 1 
    print('Actual probability of', txt, '=',
            round(1/(6**len(goal)), 8))
    est_probability = round(total/num_trials, 8)
    print('Estimated Probability of',txt,'=',round(est_probability, 8))
    
def same_date(num_people, num_same):
    possible_dates = 4*list(range(0,57)) + [58]\
        + 4*list(range(59,366)) \
            + 4*list(range(180,270))
    birthdays = [0]*366
    for p in range(num_people):
        birthdate = random.choice(possible_dates)
        birthdays[birthdate] += 1
    return max(birthdays) >= num_same

def birthday_prob(num_people, num_same, num_trials):
    num_hits = 0
    for t in range(num_trials):
        if same_date(num_people, num_same):
            num_hits += 1
    return num_hits/num_trials

for num_people in [10,20,40,100]:
    print('For',num_people,'est. prob. of a shared birthday is',
          birthday_prob(num_people,3,10000))
    numerator = factorial(366)
    denom = (366**num_people)*factorial(366-num_people)
    print('Actual prob. for N = 100 =', 1 - numerator/denom)

def std_dev(x):
    '''
    Assumes that x is a list of numbers.
    Returns the standard deviation of x
    '''
    mean = sum(x)/len(x)
    tot =0
    for num in x:
        tot += (num-mean)**2
    return (tot/len(x))**0.5 #square root of mean diff

def flip_plot(min_exp, max_exp):
    '''Assumes min_exp and max_exp are positive integers; min_exp < max_exp
Plots results of 2 ** min_exp to 2**max_exp coin flips'''
    ratios = []
    diffs = []
    xAxis = []
    for exp in range(min_exp, max_exp+1):
        xAxis.append(2**exp)
    for num_flips in xAxis:
        num_heads = 0
        for n in range(num_flips):
            if random.random() < 0.5:
                num_heads += 1
        num_tails = num_flips - num_heads
        ratios.append(num_heads/float(num_tails))
        diffs.append(abs(num_heads - num_tails))
    plt.title('Difference Between Heads and Tails')
    plt.xlabel('Number of Flips')
    plt.ylabel('Abs(#Heads - #Tails)')
    plt.semilogx(xAxis, diffs,'bo')
    plt.semilogy(xAxis, diffs,'bo')
    plt.figure()
    plt.title('Heads/Tails ratios')
    plt.xlabel('Number of Flips')
    plt.ylabel('#Heads/#Tails')
    plt.semilogx(xAxis, ratios,'bo')

random.seed(0)
# flip_plot(4,20)

def flip(num_flips):
    heads = 0
    for i in range(num_flips):
        if random.random() < 0.5:
            heads += 1
    return heads/num_flips

def flip_sim(num_flips_per_trial, num_trials):
    frac_heads = []
    for i in range(num_trials):
        frac_heads.append(flip(num_flips_per_trial))
    mean = sum(frac_heads)/len(frac_heads)
    std = std_dev(frac_heads)
    return (frac_heads, mean, std)

def label_plot(num_flips, num_trials, mean, std):
    plt.title(str(num_trials) + ' trials of ' + str(num_flips) + ' flips each.')
    plt.xlabel('Fraction of Heads')
    plt.ylabel('Number of Trials')
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    plt.text(xmin + (xmax-xmin) * 0.02, (ymax-ymin)/2,
             'Mean = ' + str(round(mean,4)) 
             + '\nSTD = ' + str(round(std,4)), size='x-large')

def make_plots(num_flips1, num_flips2, num_trials):
    val1, mean1, std1 = flip_sim(num_flips1, num_trials)
    plt.hist(val1, bins=20)
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    label_plot(num_flips1, num_trials, mean1, std1)
    plt.figure()
    val2, mean2, std2 = flip_sim(num_flips2, num_trials)
    plt.hist(val2, bins=20)
    plt.xlim(xmin,xmax)
    label_plot(num_flips2, num_trials, mean2, std2)
    
random.seed(0)
make_plots(100,1000,1000000)


def show_error_bars(min_exp,max_exp, num_trials):
    '''
    Assumes min_exp and max_exp positive ints;
        min_exp < max_exp; num_trials is a postive int;
    Plots mean fraction of heads with error bars
    '''
    means, sds = [], []
    x_vals = []
    for exp in range(min_exp, max_exp+1):
        x_vals.append(2**exp)
        frac_heads, mean, sd = flip_sim(2**exp, num_trials)
        means.append(mean)
        sds.append(sd)
    plt.errorbar(x_vals, means, yerr=2*np.array(sds))
    plt.semilogx()
    plt.title('Mean Fraction of Heads (' + str(num_trials) + ' trials)') 
    plt.xlabel('Number of flips per trial')
    plt.ylabel('Fraction of Heads & 95% confidence')
    
show_error_bars(3,10,100)

def clear(n,p,steps):
    '''
    Assumes n & steps positive ints and p a float;
        n: the initial number of molecules
        p: the probability of a molecule being cleared
        steps: the length of the simulation
    '''
    num_remaining = [n]
    for t in range(steps):
        num_remaining.append(n*((1-p)**t))
    plt.plot(num_remaining)
    plt.xlabel('Time')
    plt.ylabel('Molecules Remaining')
    plt.title('Clearance of Drug')
    
clear(1000, 0.01, 1000)

def successful_starts(event_prob, num_trials):
    '''
    Assumes event_prob is a float representing a probability
        of a single attempt being successful. num_trials a positive int
    Returns a list of the number of attempts needed before a 
        success for each trial.
    '''
    tries_before_success = []
    for t in range(num_trials):
        consec_failures = 0
        while random.random() > event_prob:
            consec_failures += 1
        tries_before_success.append(consec_failures)
    return tries_before_success

random.seed(0)
prob_of_success = 0.5
num_trials = 5000
distribution = successful_starts(prob_of_success, num_trials)
plt.hist(distribution, bins=14)
plt.xlabel('Tries Before Success')
plt.ylabel('Number of Occurrences out of ' + str(num_trials))
plt.title('Probability of Starting Each Try' + str(prob_of_success))

def play_series(num_games, team_prob):
    '''
    Assumes num_games an odd integer, team_prob a float between 0 & 1
    
    Returns True if better team wins series
    '''
    num_won = 0
    for game in range(num_games):
        if random.random() <= team_prob:
            num_won += 1
    return (num_won > num_games // 2)

def sim_series(num_series):
    prob = 0.5
    frac_won = []
    probs = []
    while prob <= 1.0:
        series_won = 0
        for i in range(num_series):
            if play_series(7,prob):
                series_won += 1
        frac_won.append(series_won/num_series)
        probs.append(prob)
        prob += 0.01
    plt.plot(probs, frac_won, linewidth=5)
    plt.xlabel('Probability of Winning a Game')
    plt.ylabel('Probability of Winning a Series')
    plt.axhline(0.95)
    plt.ylim(0.5,1.1)
    plt.title(str(num_series) + ' Seven-Game Series')
    
sim_series(400)

def find_series_length(team_prob):
    num_series = 200
    max_len = 2500
    step = 10
    
    def frac_won(team_prob, num_series, series_len):
        won = 0 
        for series in range(num_series):
            if play_series(series_len, team_prob):
                won += 1
        return won/num_series
    win_frac = []
    xvals = []
    for series_len in range(1, max_len, step):
        xvals.append(series_len)
        win_frac.append(frac_won(team_prob, num_series, series_len))
    plt.plot(xvals, win_frac, linewidth=5)
    plt.xlabel('Length of Series')
    plt.ylabel('Probability of Winning Series')
    plt.title(str(round(team_prob, 5)) + ' Probability of Better Team Winning a Game')
    plt.axhline(0.95)

yanks_prob = 0.636
phils_prob = 0.574
find_series_length(yanks_prob/(yanks_prob + phils_prob))

def collision_prob(n,k):
    prob = 1
    for i in range(1,k):
        prob = prob * ((n-i)/n)
    return 1 - prob


def sim_insertions(num_indices, num_insertions):
    '''
    Assumes num_indices and num_insertions are positive ints.
    Returns 1 if there is a collision otherwise 0
    '''
    choices = range(num_indices)
    used = []
    for i in range(num_insertions):
        has_val = random.choice(choices)
        if has_val in used:
            return 1
        else:
            used.append(has_val)
    return 0

def find_prob(num_indices, num_insertions, num_trials):
    collisions = 0
    for t in range(num_trials):
        collisions += sim_insertions(num_indices, num_insertions)
    return collisions / num_trials 

print('Actual Probability of a coliision =', collision_prob(1000, 50))
print('Est. probability of a collision =', find_prob(1000, 50, 10000))
print('Actual Probability of a collision =', collision_prob(10000, 200))
print('Est. probability of a collision =', find_prob(1000,200,10000))