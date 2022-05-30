import csv
import models
from datetime import datetime

quarterbacks = []
current_players_map = {}
current_players_list = []
current_rosters = []
current_quarterback = None
included_players = []
excluded_players = []


def read_file():
    with open('input_files/players.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                name = str.split(row[0], " (")[0]
                id = str.split(str.split(row[0], " (")[1], ")")[0]
                position = row[1]
                salary = int(row[2])
                player = models.Player(name, id, position, salary)
                if position == "QB":
                    quarterbacks.append(player.name)
                elif player not in current_players_list:
                    current_players_list.append(player.name)
            line_count += 1
   


def select_qb_display():
    global current_quarterback
    global included_players
    global excluded_players

    included_players = []
    excluded_players = []
    print("")
    print("Select a quarterback to build a roster around")
    print("")
    print("Select 0 to quit")
   
    for count, qb in enumerate(quarterbacks):
        print("Select " + str(count + 1) + " to build around " + qb)
    
    print("")
    user_input =  int(input("Select a quarterback: "))
    if user_input <= 0:
        pass
    elif user_input <= len(quarterbacks):
        current_quarterback = quarterbacks[user_input-1]
        write_quarterback_rosters(current_quarterback)
    else:
        print("You entered an invalid number")
        select_qb_display()


def write_quarterback_rosters(quarterback):
    print("")
    print("Reading the rosters for " + quarterback + " into local memeory")
    print("This may take some time...")

    with open('generated_files/' + quarterback + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            if line_count > 0:
                lcl_array = []
                for i in range(0, 11):
                    if i < 9:
                        if row[i] in current_players_map:
                            current_players_map[row[i]] += 1
                        else:
                            current_players_map[row[i]] = 1
                    lcl_array.append(row[i])
                current_rosters.append(lcl_array)
                
            line_count += 1
        select_restrictions_display()


def select_restrictions_display():
    print("")
    print("You are currently building a stack around " + current_quarterback)
    print("")
    print("There are currently " + str(len(current_rosters)) + " rosters")
    
    print("")
    print("Select 0 to restrict rosters by including a player")
    print("Select 1 to restrict rosters by excluding a player")
    print("Select 2 to quit without writing a csv")
    print("")
    user_input = int(input("Select an option: "))

    if user_input == 0:
        player_restriction_display("include")
    elif user_input == 1:
        player_restriction_display("exclude")
    else:
        pass


def player_restriction_display(type):
    global current_rosters
    lcl_roster_array = []
    procede = False
    print("")
    print("Select a player to " + type)
    for count, player in enumerate(current_players_list):
        if player in current_players_map:
            print("Select " + str(count) + " to " + type + " " + player + 
            "- currently on " + str(current_players_map[player]) + " rosters")
    print("")
    user_input = int(input("Select a player: "))
    if user_input >= 0 and user_input < len(current_players_list):
        if current_players_list[user_input] is not None:
            procede = True
            if type == "include":
                included_players.append(current_players_list[user_input])
            else:
                excluded_players.append(current_players_list[user_input])
        else:
            print("You have selected an invalid number, please select again")
            print("")
            player_restriction_display(type)
    else:
        print("You have selected an invalid number, please select again")
        print("")
        player_restriction_display(type)
    
    if procede:
        for roster in current_rosters:
            if set(included_players).issubset(set(roster)):
                if not bool(set(excluded_players) & set(roster)):
                    lcl_roster_array.append(roster)
        if len(lcl_roster_array) > 0:
            current_rosters = lcl_roster_array
            write_restrict_quit_display()
        else:
            print("This is not a posiblity with the restrictions you've selected.")
            print("")
            excluded_players.pop()
            player_restriction_display(type)
         
        
   
def write_restrict_quit_display():
    global current_players_map
    lcl_map = {}
    lcl_list = []
    for roster in current_rosters:
        for i in range(1, 11):
            if i < 9:
                lcl_list.append(roster[i])
                if roster[i] in lcl_map:
                    lcl_map[roster[i]] += 1
                else:
                    lcl_map[roster[i]] = 1
    current_players_map = lcl_map
    print("")
    print("There are currently " + str(len(current_rosters)) + 
    " remaining from the restrictions you have selected")
    print("")
    if len(included_players) > 0:
        print("These are the players that are included in every roster:")
        print("")
        for count, element in enumerate(included_players):
             print(str(count+1) + ". " + element )
    print("")
    if len(excluded_players) > 0:
        print("These are the players that are excluded from every roster:")
        print("")
        for count, element in enumerate(excluded_players):
             print(str(count+1) + ". " + element )
    print("")
    print("Here is a breakdown of the current rosters:")
    print(str(current_players_map))
    print("")
    if len(current_rosters) > 1:
        print("Select 0 to continue to restrict the rosters")
    print("Select 1 to write a csv file of the rosters and build a new stack")
    print("Select 2 to write a csv file of the rosters and end the program")
    print("Select 3 to quit and NOT write a csv file")
    print("")
    user_input = int(input("Select an option: "))

    if user_input == 0:
        select_restrictions_display()
    elif user_input == 1:
        write_csv()
        select_qb_display()
    elif user_input == 2:
        write_csv()
        print("The building stacks script has terminated")
    else:
         print("The building stacks script has terminated")

def write_csv():
    now = str(datetime.now())
    
    with open('output_files/' + current_quarterback + '.' + now +  '.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FX', 'DST', 'Budget', 'Projection'])

        # write multiple rows
        writer.writerows(current_rosters)
          
    print("The csv file is complete")

def run_restrict():
    read_file()
    select_qb_display()
