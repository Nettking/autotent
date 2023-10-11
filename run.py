import subprocess
import os

def run_python_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")
    except Exception as e:
        print(f"An error occurred while running script {script_path}: {e}")

if __name__ == "__main__":
    print("Running AutoTent 1.0.0 Initial Release")
    print("Select a program to run")
    if os.name == 'posix':  # Linux and macOS
        script_paths = [
            'sensor_readings/soil_moisture/process_raw_data/calculate_error.py',
            'sensor_readings/soil_moisture/process_raw_data/graph_error.py',
            'tools/set_headertext.py'
        ]
    else: # Windows
        script_paths = [
            'sensor_readings\soil_moisture\process_raw_data\calculate_error.py',
            'sensor_readings\soil_moisture\process_raw_data\graph_error.py',
            'tools\set_headertext.py'
        ]
    menu_options = [
        "1. Calculate Error",
        "2. Graph Error",
        "3. Set Header Text"
    ]

    for option in menu_options:
        print(option)

    selected_number = int(input("Select a program to run: "))
    selected_program = script_paths[selected_number-1] # Subtract 1 due to index start at 0
    run_python_script(selected_program)
    


