
class KnockoutStage():
    """class of knockout stage matches"""
    def __init__(self, round_name, matches):
        self.round_name = round_name
        self.matches = matches
    
    def play_round(self):
        """Play every match in this knockout round"""
        for match in self.matches:
            match.play()
        
    def get_winners(self):
        """Returns:
        list:
            Winners of all matches.
        """
        winners = []
        for match in self.matches:
            winners.append(match.winner)
        return winners
            
    def display_results(self):
        """displaying match results of each match of the stage"""
        for match in self.matches:
            print(f"\n{match.team1.name:>12} {match.goals1} - {match.goals2} {match.team2.name:<12}"
                  f" {f'({match.team1.penalty_goals} - {match.team2.penalty_goals} pens)' if match.go_penalties else '            '}"
                  f" winner: {match.winner.name}")