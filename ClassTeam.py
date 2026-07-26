import numpy as np
class Team():
    """represents national football teams and their information """
    def __init__(self, name, attack, defense, rank):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank

        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = ""
        self.penalty_goals = 0 ## for printing penalty goals

    def goal_difference(self):
        """goal difference calculation"""
        return self.goals_for - self.goals_against
    
    def reset_stats(self):
        """resets the teams stats"""
        self.goals_against = 0
        self.goals_for = 0
        self.points = 0
        self.group = ''
        self.penalty_goals = 0
        
    def simulate_match(self, opponent, is_knockout = False):
        """simulating the matches anf returns its results
        args: opponent team , is_knockout (True or False)

        returns: goals of self team, goals of opponent team , winner of the match
        """
        self.go_penalties = False  #the flag that shows the match has gone to penalties or not
        
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense/100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense/100) * 0.8
        
        self_goals = np.random.poisson(lambda_self)         #the number of self team goals
        opponent_goals = np.random.poisson(lambda_opponent) #the number of opponent team goals
        
        
        if self_goals > opponent_goals:
                winner = self
        elif self_goals < opponent_goals:
                winner = opponent
        else :
            winner = None
            
        if not is_knockout:
            if winner == self:
                self.points += 3
            elif winner == opponent:
                opponent.points += 3
            elif winner is None:
                self.points +=1
                opponent.points += 1
                
        if is_knockout and winner is None:                  #Extra time
            extra_lambda_self = lambda_self * (1/3)
            extra_lambda_opponent = lambda_opponent * (1/3)
            
            self_goals += np.random.poisson(extra_lambda_self)
            opponent_goals += np.random.poisson(extra_lambda_opponent)
            
            if self_goals > opponent_goals:
                winner = self
            elif self_goals < opponent_goals:
                winner = opponent
            else :
                winner = None
            
        self.goals_for += self_goals
        self.goals_against += opponent_goals
        opponent.goals_for += opponent_goals
        opponent.goals_against += self_goals
        
        if is_knockout and winner is None: #penalties
            self.go_penalties = True
            
            penalty_chance_self = 0.75 + (self.attack - opponent.defense) / 250
            p_self = np.clip(penalty_chance_self, 0.6 , 0.9)    #np.clip is for rounding the num between 0.6 & 0.9

            penalty_chance_opponent = 0.75 + (opponent.attack - self.defense) / 250
            p_opponent = np.clip(penalty_chance_opponent ,0.6 ,0.9)
            
            opponent.penalty_goals = 0
            self.penalty_goals = 0
            
            for _ in range(0,5):
                rand_num_self = np.random.random()
                if rand_num_self < p_self:
                    self.penalty_goals += 1
                
                rand_num_opponent = np.random.random()
                if rand_num_opponent < p_opponent:
                    opponent.penalty_goals += 1
                
            if self.penalty_goals == opponent.penalty_goals:
                while self.penalty_goals == opponent.penalty_goals:
                    rand_num_self = np.random.random()
                    if rand_num_self < p_self:
                        self.penalty_goals += 1

                    rand_num_opponent = np.random.random()
                    if rand_num_opponent < p_opponent:
                        opponent.penalty_goals += 1
                        
            if self.penalty_goals > opponent.penalty_goals:
                    winner = self
            
            elif self.penalty_goals < opponent.penalty_goals:
                    winner = opponent

            self.penalties = (self.penalty_goals , opponent.penalty_goals)   
            
        return self_goals , opponent_goals , winner