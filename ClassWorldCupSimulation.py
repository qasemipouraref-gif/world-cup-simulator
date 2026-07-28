import csv
import random 

from ClassTeam import Team
from ClassMatch import Match
from ClassGroup import Group
from ClassKnockoutStage import KnockoutStage

class WorldCupSimulator():
    """main class of simulating the world cup"""
    def __init__(self):
        self.teams = []
        self.groups = []
        
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        
        self.knockout_stage = None
        self.champion = None
    
    def load_teams_from_csv(self, filename):
        """reading the CSV file and loading teams"""
        self.teams = []
        try:
            with open(filename, mode = "r" ,newline = "", encoding= "utf-8" ) as file: 
                reader = csv.DictReader(file)
            
                for row in reader: # putting teams specification into the variables
                    name = row["name"]
                    attack = int(row["attack"])
                    defense = int(row["defense"])
                    rank = int(row["rank"])
                
                    team = Team(name, attack, defense, rank)
                    self.teams.append(team)
        except FileNotFoundError:
            print("CSV File not found")
            return False
        
        except KeyError:
            print("CSV format is incorrect")
            return False
        
        except ValueError:
            print("CSV has invalid Data")    
            return False
        if len(self.teams) != 32:
            print("CSV must contain 32 teams")
            self.teams = [  ]
            return False
        return True
            
    def seed_and_draw_groups(self):
        """putting teams in 4 seeds and draw 8 groups"""
        self.groups = []
        
        self.teams.sort(key= lambda team: team.rank) # if the teams were not ranked properly
        
        seed1 = random.sample(self.teams[:8], 8)
        seed2 = random.sample(self.teams[8:16], 8)
        seed3 = random.sample(self.teams[16:24], 8)
        seed4 = random.sample(self.teams[24:], 8)
        
        group_names = ["A","B","C","D","E","F","G","H",]
        
        for i in range(8):
            teams = [seed1[i], seed2[i], seed3[i], seed4[i]]
            group = Group(group_names[i] , teams)
            
            for team in teams: # for teams' group name (self.group in Team Class)
                team.group = group.name
            
            self.groups.append(group)

    def run_group_stage(self, show_output = True):
        """playing the group matches printing the groups schedule"""
        for group in self.groups: # playing  the matches and ranking the teams in group
            group.play_all_matches()
            ranking = group.get_ranking()
            if show_output: 
                print(f"Group {group.name}")
                print("-------------------")
                print(f"{'Team':<12} points  GF GA GD")
                  
                for team in ranking:
                    print(f"{team.name:<12}  {team.points:<6} {team.goals_for:<2} {team.goals_against:<2} {team.goal_difference():>2}")
                print()

    def setup_knockout_stage(self):
        """setting up the knockout stages"""
        self.knockout_stage = KnockoutStage("Round of 16" , [])

        qualified = []
        for group in self.groups: #choosing the first and the second team for knockout stages
            first, second = group.advance_teams()
            qualified.append((first, second))
            
        pairings = [(0,1) ,(2,3) ,(4,5) ,(6,7) ,(1,0) ,(3,2) ,(5,4) ,(7,6)] #pairing teams for playing matches
        
        for first_group , second_group in pairings:
            team1 = qualified[first_group][0]
            team2 = qualified[second_group][1]
            
            match = Match(team1, team2, is_knockout=True)
            self.knockout_stage.matches.append(match)

    def run_knockout_stage(self, show_output = True):
    
        current_matches = self.knockout_stage.matches
        round_names = ["Round of 16", "Quarterfinals" , "Semifinals" , "Final"]

        for index , round_name in enumerate(round_names):
            stage = KnockoutStage(round_name , current_matches)

            if index == 0:
                self.round_of_16 = stage
            elif index == 1:
                self.quarterfinals = stage
            elif index == 2:
                self.semifinals = stage 
            else:
                self.final = stage

            stage.play_round()
            winners = stage.get_winners()
            

            if show_output:
                print(f"\n==== {round_name} ====")
                stage.display_results()

            if len(winners) == 1:
                self.champion = winners[0]
                if show_output:
                    print(f"\nChampion: {self.champion.name}")
                break
            
            next_matches = []
            for i in range(0 , len(winners), 2): #advancing teams for next stage
                next_matches.append(Match(winners[i] , winners[i + 1], is_knockout = True))

            current_matches = next_matches

    def run_full_simulation(self, show_output = True):
        """simulating the whole world cup and returning the champion"""
        self.champion = None
        for team in self.teams:
            team.reset_stats() # resets the teams stats if there was a simulation before
            
        self.seed_and_draw_groups()
        self.run_group_stage(show_output)
        self.setup_knockout_stage()
        self.run_knockout_stage(show_output)

        return self.champion

    def most_likely_champion(self , num_simulations = 1000):
        """calculating the chances of teams winning world cup"""
        champions = {}
        for _ in range(num_simulations):
            self.run_full_simulation(show_output=False)
            name = self.champion.name

            if name in champions: #counting the number of winnings
                champions[name] += 1
            else:
                champions[name] = 1

        sorted_champions = sorted(champions.items() , key = lambda item: item[1], reverse=True) 
        #sorting teams based on the number of winning the world cup

        print(f"\nMost likely champion:\n")

        for team_name , wins in sorted_champions:
            percentage = (wins / num_simulations) * 100
            print(f"{team_name:<15}: {percentage:.2f}%")

    def display_bracket(self):
        """displaying the bracket of last simulation of world cup knockout stage"""
        stages = [self.round_of_16 , self.quarterfinals ,self.semifinals , self.final]

        for stage in stages:
            if stage is None:
                continue
            print(f"\n===={stage.round_name}====")

            for match in stage.matches:
                print(f"\n{match.team1.name:>12} {match.goals1} - {match.goals2} {match.team2.name:<12}"
                      f" {f'({match.team1.penalty_goals} - {match.team2.penalty_goals} pens)' if match.go_penalties else '            '}"
                      f" winner: {match.winner.name}")

        if self.champion:
            print(f"\nChampion: {self.champion.name}")

    def display_groups(self):
        """displays groups after seed and draw"""
        print("=====Groups=====")

        for i , group in enumerate(self.groups):
            print(f"group {chr(65 + i)}:")
            for team in group.teams:
                print(f" - {team.name}")
            print()
