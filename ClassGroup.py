from ClassMatch import Match
import random
class Group():
    """class of world cup teams groups"""
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        
    def play_all_matches(self):
        """plays all of the matches that 4 teams of a groups should play"""
        for i in range(4): # playing matches for each team and not playing a game repeatedly
            for j in range(i+1,4):
                match = Match(self.teams[i], self.teams[j])
                match.play()
    
    def get_ranking(self):
        """ranking the teams based on their points, GD , GF and random"""
        teams = random.sample(self.teams, len(self.teams))
        ranking = sorted(teams, key=lambda team:(team.points, team.goal_difference(), team.goals_for), reverse=True)
        return ranking
    
    def advance_teams(self):
        """advancing the first and the second team for knockout stages"""
        ranking = self.get_ranking()
        return ranking[0], ranking[1]