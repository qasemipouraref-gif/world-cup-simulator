# FINAL PROJECT

#=============================
# دانشجو : عارف قاسمی پور
# شماره دانشجویی : 404131083
# عنوان : شبیه ساز جام جهانی
# 1405/5/4 :تاریخ تحویل 
#=============================

from ClassWorldCupSimulation import WorldCupSimulator

def main():
    simulator = WorldCupSimulator()

    teams_loaded = False
    groups_drawn = False

    while True:
        print("\n===== WorldCup Simulator =====")
        print("1. Load teams from CSV")
        print("2. seed and draw groups")
        print("3. Run group stage")
        print("4. run full simulation")
        print("5. Most likely champion")
        print("6. Display bracket")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter CSV file: ")
            success = simulator.load_teams_from_csv(filename)
            if success:
                teams_loaded = True
                print(f"\nTeams loaded successfully")
            else:
                print(f"\nError loading file")

        elif choice == "2":
            if not teams_loaded:
                print(f"\nLoad teams first")
            else:
                simulator.seed_and_draw_groups()
                simulator.display_groups()
                groups_drawn = True
                print(f"\nTeams has been drawn successfully")

        elif choice == "3":
            if not teams_loaded:
                print(f"\nLoad teams first")
                continue
            if not groups_drawn:
                print(f"\nDraw groups first")
                continue
            else:
                simulator.run_group_stage()

        elif choice == "4":
            if not teams_loaded:
                print(f"\nLoad teams first")
                continue
            simulator.run_full_simulation()

        elif choice == "5":
            if not teams_loaded:
                print(f"\nLoad teams first")
                continue
            try:
                num = int(input("Number of simulations: "))
                
            except ValueError:
                print("please enter a valid NUMBER!")
                continue
            
            if num < 1:
                print(f"\nError for number of simulations")
                continue

            simulator.most_likely_champion(num)

        elif choice == "6":
            if not teams_loaded:
                print(f"\nLoad teams first")
                continue

            simulator.display_bracket()

        elif choice == "7":
            print(f"\nGoodBye!")
            break
        else:
            print(f"\nInvalid choice")

if __name__ == "__main__":
    main()
