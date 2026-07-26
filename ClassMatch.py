
class Match():
    """a class for playing the match and updating teams stats and determining the winner"""
    def __init__(self, team1, team2, is_knockout=False):
        self.team1 = team1
        self.team2 = team2
        self.is_knockout = is_knockout
        self.goals1 = None
        self.goals2 = None
        self.winner = None

    def play(self):
        """Plays one football match.
            Returns:
                tuple:
                    goals scored by team1,
                    goals scored by team2,
                    winner team"""
        
        self.goals1, self.goals2, self.winner = self.team1.simulate_match(self.team2, self.is_knockout)
        self.go_penalties = self.team1.go_penalties
            
        return self.goals1, self.goals2, self.winner