import os.path
from logic_create import run_create
from logic_restrict import run_restrict

user_input = 0

path = os.path.exists('generated_files/player_breakdown.csv')

if path:
    print("Currently you have files in the generated_files folder")
    print("")
    print("Select 1 to rewrite the files")
    print("Select 2 to use these files to start building stacks")
    print("")
    user_input = int(input("Make a selection: "))
    if user_input == 1:
        run_create()
    elif user_input == 2:
        print("We will now build stacks")
    else:
        print("This is not a valid selection")
else:
    run_create()

path = os.path.exists('generated_files/player_breakdown.csv')
print("")
if path and user_input == 2:
    run_restrict()
else:
    print("The script has terminated")