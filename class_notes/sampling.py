import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import integrate
from math import pi, e 

def get_bm_data(filename):
    '''
    Read the contents of the given file. Assumes the file in a comma-separated format,
    with 6 elements in entry:
    0.Name (string), 1. Gender (str), 2. Age (Int),
    3.Division(int), 4. Country(string), 5. Overall Time (float)
    Returns: Dict containing a list for each of the six varialbes
    '''
    data = {}
    f = open(filename)
    line = f.readline()
    data['name'], data['gender'], data['age'] = [],[],[]
    data['division'], data['country'], data['time'] = [],[],[]
    while line != '':
        split = line.split(',')
        data['name'].append(split[0])
        data['gender'].append(split[1])
        data['age'].append(split[2])
        data['division'].append(int(split[3]))
        data['country'].append(split[4])
        data['time'].append(float(split[5][:-1]))
        line = f.readline()
    f.close()
    return data

def make_hist(data, bins, title, xlabel, ylabel):
    plt.hist(data, bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    mean = sum(data)/len(data)
    stdv = np.std(data)
    plt.annotate('Mean = ' + str(round(mean, 2)) + \
        '\nSD = ' + str(round(stdv, 2)), fontsize=20,
        xy = (0.65, 0.75), xycoords='axes fraction')
    
def sample_times(times, num_examples):
    '''
    Assumes times a list of floats representing finishing
    times of all runners. num_examples an int
    Generates a random sample of size num_examples, and produces
    a histogram showing the distribution along with its mean and standard deviation
    '''
    sample = random.sample(times, num_examples)
    make_hist(sample, 10, 'Sample of Size ' + str(num_examples),
              'Minutes to Complete Race', 'Number of Runners')
    
times = get_bm_data(r'C:\Users\Tyler Dufrene\OneDrive\Documents\TylerDufrene\OSSU - DataScience\class_notes\bm_results2012.txt')['time']
make_hist(times,20,'2012 Boston Marathon', 
          'Minutes to Complete Race', 'Number of Runners')

sampleSize = 40
sample_times(times, sampleSize)

def gaussian(x, mu, sigma):
    factor1 = (1/(sigma*((2*pi)**0.5)))
    factor2 = e**-(((x-mu)**2)/(2*sigma**2))
    return factor1 * factor2

area = round(integrate.quad(gaussian, -3,3,(0,1))[0],4)
print('Probability of being within 3 of true mean of tight dist. =', area)
area = round(integrate.quad(gaussian,-3,3, (0,100))[0],4)
print('Probability of being within 3 of true mean of wide dist. =', area)

def test_samples(num_trials, sample_size):
    tight_means, wide_means = [],[]
    for t in range(num_trials):
        sample_tight, sample_wide = [],[]
        for i in range(sample_size):
            sample_tight.append(random.gauss(0,1))
            sample_wide.append(random.gauss(0,100))
        tight_means.append(sum(sample_tight)/len(sample_tight))
        wide_means.append(sum(sample_wide)/len(sample_wide))
    return tight_means, wide_means

tight_means, wide_means = test_samples(1000,40)
plt.plot(wide_means, 'y*', label = 'SD = 100')
plt.plot(tight_means,'bo', label = 'SD = 1')
plt.xlabel('Sample Number')
plt.ylabel('Sample Mean')
plt.title('Means of Samples of Size ' + str(40))
plt.legend()
plt.figure()
plt.hist(wide_means, bins=20, label = 'SD = 100')
plt.title('Distribution of Sample Means')
plt.xlabel('Sample Mean')
plt.ylabel('Frequency of Occurence')
plt.legend()

def plot_means(num_dice_per_trial, num_dice_thrown, num_bins, legend,color, style):
    means = []
    num_trials = num_dice_thrown//num_dice_per_trial
    for i in range(num_trials):
        vals = 0
        for j in range(num_dice_per_trial):
            vals += 5*random.random()
        means.append(vals/num_dice_per_trial)
    plt.hist(means, num_bins, color=color, label=legend, weights=np.array(len(means)*[1])/len(means),
             hatch=style)
    return sum(means)/len(means), np.var(means)

mean, variance = plot_means(1,100000, 11, '1 die', 'w', '*')
print('Mean of rolling 1 die =', round(mean,4),
      'Variance =',round(variance,4))
mean, variance = plot_means(100,100000, 11, '100 die', 'w', '//')
print('Mean of rolling 100 die =', round(mean,4),
      'Variance =',round(variance,4))
plt.title('Rolling Continuous Dice')
plt.xlabel('Value')
plt.ylabel('Probability')
plt.legend()

mean_of_means, std_of_means = [],[]
sample_sizes = range(50,2000,200)
for sample_size in sample_sizes:
    sample_means = []
    for t in range(20):
        sample = random.sample(times, sample_size)
        sample_means.append(sum(sample)/sample_size)
    mean_of_means.append(sum(sample_means)/len(sample_means))
    std_of_means.append(np.std(sample_means))
plt.errorbar(sample_sizes, mean_of_means, yerr=1.96*np.array(std_of_means),
             label='Estimated mean and 95% confidence interval')
plt.xlim(0,max(sample_sizes) + 50)
plt.axhline(sum(times)/len(times), linestyle='--',
            label = 'Population mean')
plt.title('Estimates of Mean Finishing Time')
plt.xlabel('Sample Size')
plt.ylabel('Finishing Time (minutes)')
plt.legend(loc='best')


pop_std = np.std(times)
sample_sizes = range(2,200,2)
diff_means = []
for sample_size in sample_sizes:
    diffs = []
    for t in range(100):
        diffs.append(abs(pop_std - np.std(random.sample(times, sample_size))))
    diff_means.append(sum(diffs)/len(diffs))
plt.plot(sample_sizes, diff_means)
plt.xlabel('Sample Size')
plt.ylabel('Abs(Pop.Std - Sample Std)')
plt.title('Sample SD vs Population SD')


pop_mean = sum(times) / len(times)
sample_size = 200
num_bad = 0
for t in range(10000):
    sample = random.sample(times, sample_size)
    sample_mean = sum(sample)/sample_size
    se = np.std(sample)/sample_size**0.5
    if abs(pop_mean - sample_mean) > 1.96*se:
        num_bad +=1
print('Fraction outside 95% confidence interval =', num_bad/10000)