import random

def roll_die():
    return random.choice([1,2,3,4,5,6])    

def check_pascal(num_trials):
    '''
    Assumes num_trials >=0
    Prints an estimate of the probability of winning
    '''
    num_wins = 0
    for i in range(num_trials):
        for j in range(24):
            d1 = roll_die()
            d2 = roll_die()
            if d1 == 6 and d2 == 6:
                num_wins += 1
                break
    print('Probability of winning =', num_wins/num_trials)
    
class CrapsGame(object):
    def __init__(self):
        self.pass_wins, self.pass_losses = (0,0)
        self.dp_wins, self.dp_losses, self.dp_pushes = (0,0,0)
        
    def play_hand(self):
        points_dict = {
            4:1/3,
            5:2/5,
            6:5/11,
            8:5/11,
            9:2/5,
            10:1/3
        }
        throw = roll_die() + roll_die()
        if throw == 7 or throw == 11:
            self.pass_wins +=1 
            self.dp_losses += 1
        elif throw == 2 or throw ==3 or throw == 12:
            self.pass_losses += 1
            if throw == 12:
                self.dp_pushes += 1
            else:
                self.dp_wins += 1
        else:
            if random.random() <= points_dict[throw]:
                self.pass_wins += 1
                self.dp_losses += 1
            else:
                self.pass_losses += 1
                self.dp_wins +=1
                
    def pass_results(self):
        return (self.pass_wins, self.pass_losses)
    
    def dp_results(self):
        return (self.dp_wins, self.dp_losses, self.dp_pushes)
    
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

                    
def craps_sim(hands_per_game, num_games):
    '''
    Assumes hands_per_game and num_games are ints >= 0
    Play num_games of hands_per_game, and print results
    '''
    games = []
    
    #play num_games
    for t in range(num_games):
        c = CrapsGame()
        for i in range(hands_per_game):
            c.play_hand()
        games.append(c)
        
    # Produce statistics for each game
    p_ROI_per_game, dp_ROI_per_game = [],[]
    for g in games:
        wins, losses = g.pass_results()
        p_ROI_per_game.append((wins-losses)/hands_per_game)
        wins, losses, pushes = g.dp_results()
        dp_ROI_per_game.append((wins-losses)/hands_per_game)
        
    # Produce and print summary statistics
    mean_roi = str(round((100*sum(p_ROI_per_game)/num_games), 4)) + '%'
    sigma = str(round(100*stdDev(p_ROI_per_game), 4)) + '%'
    print('Pass:', 'Mean ROI =', mean_roi, 'Std Dev. =', sigma)
    mean_roi = str(round((100*sum(dp_ROI_per_game)/num_games), 4)) + '%'
    sigma = str(round(100*stdDev(dp_ROI_per_game), 4)) + '%'
    print('Don\'t Pass:', 'Mean ROI =', mean_roi, 'Std Dev. =', sigma)
    
    
def throw_needles(num_needles):
    in_circle = 0
    for needles in range(1,num_needles+1,1):
        x = random.random()
        y = random.random()
        if (x*x + y*y) ** 0.5 <= 1:
            in_circle += 1
    # counting needles in one quadrant only, multiply by 4
    return 4 * (in_circle/num_needles)

def get_est(num_needles, num_trials):
    estimates = []
    for t in range(num_trials):
        pi_guess = throw_needles(num_needles)
        estimates.append(pi_guess)
    st_dev = stdDev(estimates)
    cur_est = sum(estimates)/len(estimates)
    print('Est. = ' + str(round(cur_est, 5)) + \
        ', Std. Dev = ' + str(round(st_dev,5))\
            + ', Needles = ' + str(num_needles))
    return (cur_est, st_dev)

def est_pi(precision, num_trials):
    num_needles = 1000
    std = precision 
    while std >= precision/2:
        cur_est, std = get_est(num_needles, num_trials)
        num_needles *= 2
    return cur_est
    
    
class FairRoulette():
    def __init__(self):
        self.pockets = []
        for i in range(1,37):
            self.pockets.append(i)
        self.ball = None 
        self.pocketOdds = len(self.pockets) - 1
    def spin(self):
        self.ball = random.choice(self.pockets)
    def bet_pocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt * self.pocketOdds
        else: return -amt 
    def __str__(self):
        return 'Fair Roulette'
    
def play_roulette(game, num_spins, pocket, bet, to_print):
    tot_pocket = 0
    for i in range(num_spins):
        game.spin()
        tot_pocket += game.bet_pocket(pocket, bet)
    if to_print:
        print(num_spins, 'spins of', game)
        print('Expected Return betting', pocket,'='\
            , str(100*tot_pocket/num_spins) + '%\n')
    return (tot_pocket/num_spins)

random.seed(0)
game = FairRoulette()
for num_spins in (100,10000000):
    for i in range(3):
        play_roulette(game, num_spins, 2,1,True)
        
result_dict = {}
games = ()