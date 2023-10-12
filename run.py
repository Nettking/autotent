
from config import *

def main():

    script_paths, menu_options = set_script_paths_and_menu_options()

    for option in menu_options:
        print(option)

    selected_number = int(input("Select a program to run: "))
    selected_program = script_paths[selected_number-1] # Subtract 1 due to index start at 0
    run_python_script(selected_program)

if __name__ == "__main__":
    main()
    


