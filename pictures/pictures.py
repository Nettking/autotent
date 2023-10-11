import subprocess
import os
import datetime
import time

run_directory = "/mnt/c/wsl/pictures/"

def print_and_log(message):
    log = run_directory + "log"
    with open(log, "a") as log_file:
        log_entry = message + '\n'
        log_file.write(log_entry)
    print(message)


def rename_file_with_date(prefix, old_filename="pic1.png"):
    # Get the current date in the format YYYYMMDD
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # Split the old filename into name and extension
    name, extension = os.path.splitext(old_filename)

    # Create the new filename
    new_filename = prefix + current_date + extension

    # Rename the file
    os.rename(old_filename, new_filename)


def collect_picture(client_adress, client_path, prefix):
    # The ssh command to execute raspistill
    ssh_raspistill_command = ["ssh", client_adress, "raspistill", "-o", "pic1.png"]

    # The scp command to execute
    scp_command = ["scp", client_path, "./"]

    # The ssh command to delete the image
    ssh_rm_command = ["ssh", client_adress, "rm", "pic1.png"]

    # Execute the ssh raspistill command
    ssh_raspistill_result = subprocess.run(ssh_raspistill_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check the result of the ssh raspistill command
    if ssh_raspistill_result.returncode != 0:
        message = "SSH raspistill command failed with error: "+ ssh_raspistill_result.stderr.decode()
        print_and_log(message)
    else:
        # If the ssh raspistill command was successful, execute the scp command
        scp_result = subprocess.run(scp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Check the result of the scp command
        if scp_result.returncode != 0:
            message = "SCP command failed with error: "+ scp_result.stderr.decode()
            print_and_log(message)
        else:
            # If the scp command was successful, delete the original image
            ssh_rm_result = subprocess.run(ssh_rm_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Check the result of the ssh delete command
            if ssh_rm_result.returncode != 0:
                message = "SSH delete command failed with error: " + ssh_rm_result.stderr.decode() 
                print_and_log(message)
            else:
                rename_file_with_date(prefix, "pic1.png")
                message = "Image copied and deleted successfully from " + client_adress
                print_and_log(message)

def collect_all():
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    message = current_date + ": Collection started"
    print_and_log(message)

    client_adress_top_camera = "nettking@192.168.0.141"
    client_path_top_camera = client_adress_top_camera + ":/home/nettking/pic1.png" 
    prefix_top_camera = "top_"

    client_adress_side_camera = "pi@192.168.0.105"
    client_path_side_camera = client_adress_side_camera + ":/home/pi/pic1.png"
    prefix_side_camera = "side_"

    collect_picture(client_adress_top_camera, client_path_top_camera, prefix_top_camera)
    collect_picture(client_adress_side_camera, client_path_side_camera, prefix_side_camera)

def init_monitoring():
    now = datetime.datetime.now().time()
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    print_string = date_string + ": Started at " + str(now.hour) + ":" + str(now.minute)
    message = print_string
    print_and_log(message)

init_monitoring()
collect_all()
while True:
    try:
        # Get the current time
        now = datetime.datetime.now().time()
        
        # Check if it's 05:59
        if (now.hour == 5 and now.minute == 59):
            # Capture the image
            collect_all()
            now_str = datetime.datetime.now()
            date_string = now_str.strftime("%Y-%m-%d")
            message = 'picture taken at ' + date_string 
            print_and_log(message)
            
            # Sleep for 1 minute to prevent multiple captures in the same minute
            time.sleep(60)

        # Sleep for 1 second before checking the time again
        time.sleep(1)
    except:
        pass