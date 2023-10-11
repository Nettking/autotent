import subprocess
import os

def set_script_paths_and_menu_options():
    common_path = 'sensor_readings' + os.sep + 'soil_moisture' + os.sep + 'process_raw_data'
    multi_sensor_path = 'sensor_readings' + os.sep + 'multi_sensor'
    script_paths = [        
        os.path.join(common_path, 'calculate_error.py'),
        os.path.join(common_path, 'graph_error.py'),
        os.path.join(multi_sensor_path, 'graph_data.py'),
        os.path.join('tools', 'set_headertext.py')
    ]
    
    menu_options = [
        "1. Calculate Error",
        "2. Graph Error",
        "3. Graph data",
        "4. Set Header Text"
        
    ]
    
    return script_paths, menu_options

def run_python_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")
    except Exception as e:
        print(f"An error occurred while running script {script_path}: {e}")

def main():
    print("Running AutoTent 1.0.0 Initial Release")
    print("Select a program to run")
    
    script_paths, menu_options = set_script_paths_and_menu_options()

    for option in menu_options:
        print(option)

    selected_number = int(input("Select a program to run: "))
    selected_program = script_paths[selected_number-1] # Subtract 1 due to index start at 0
    run_python_script(selected_program)

if __name__ == "__main__":
    main()
    


