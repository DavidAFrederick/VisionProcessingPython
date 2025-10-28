import os
import csv

import paramiko
from scp import SCPClient, SCPException
import socket
import sys
from datetime import datetime
import time


class file_transfer_status():
   NEW                = 1
   READY_FOR_TRANSFER = 2
   TRANSFERRED        = 3
   READY_FOR_DELETION = 4
   DELETED            = 5

video_log_directory_path = "/home/a/vision_movement_files/"  
file_list_data_file_DB = "file_list_data_file_DB.txt"
full_db_file_name = video_log_directory_path + file_list_data_file_DB

audit_log_file_path = "/home/a/vision_file_management_audit_logs/"
audit_log_file_name = "initial_log_file.txt"
audit_log_full_file_name = ""

file_list_data = []
new_file_list_data = []

# #---------------------------------------------------------------------------------------------
def create_a_list_of_file_information() -> list:
    global file_list_data

    # List all files and directories
    new_file_list_data =[]
    all_entries = sorted(os.listdir(video_log_directory_path))
    file_status = file_transfer_status.NEW

    for entry in all_entries:
        full_entry_name = video_log_directory_path + entry
        file_size_bytes = os.path.getsize(full_entry_name)
        new_file_list_data.append([full_entry_name, file_size_bytes, file_status])

    print(f"Creating new List of File Information by reading entries from the disk {len(new_file_list_data)} rows")
    return new_file_list_data

# #---------------------------------------------------------------------------------------------

def print_list_of_file_information_to_screen(file_list_data_to_print : list, note : str):
    # global file_list_data
    print("----------------------------------------------------")
    # print (file_list_data_to_print)
    # print(f" file_list_data_to_print [0][0]  {file_list_data_to_print [0][0] }")
    # print(f" file_list_data_to_print [0][1]  {file_list_data_to_print [0][1] }")
    # print(f" file_list_data_to_print [0][2]  {file_list_data_to_print [0][2] }")
    # print(f" file_list_data_to_print [1][0]  {file_list_data_to_print [1][0] }")
    # print(f" file_list_data_to_print [1][1]  {file_list_data_to_print [1][1] }")
    # print(f" file_list_data_to_print [1][2]  {file_list_data_to_print [1][2] }")

    if (file_list_data_to_print != None):
        print (f"NOTE: {note}     Number Rows: {len(file_list_data_to_print)}")
        for row_of_data in file_list_data_to_print:
            print (f"{row_of_data}     {note}")
    else:
        print(f"NOTE: {note}  The list is empty")

# #---------------------------------------------------------------------------------------------
def write_list_of_file_information_to_disk(file_list_data_to_disk : list):
    
    # Write the list of lists to a CSV file
    with open(full_db_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(file_list_data_to_disk)
    print(f"Writing CSV file to  to disk.  {len(file_list_data_to_disk)} rows")

# #---------------------------------------------------------------------------------------------
def read_list_of_file_information_from_disk() -> list:
    
    file_list_data = []
    
    with open(full_db_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            file_list_data.append(row)

    print (f"{len(file_list_data)} rows of in List read from the disk")
    return file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_existing_database_or_create_new_one():
    global file_list_data
    try:
        file_list_data = read_list_of_file_information_from_disk()
        write_to_audit_log_and_close(audit_log_full_file_name, "Data file found.")

    except FileNotFoundError:
        write_to_audit_log_and_close(audit_log_full_file_name, "Data file not found.  Creating new database")


        file_list_data = create_a_list_of_file_information()
        write_list_of_file_information_to_disk(file_list_data)

    return file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def create_new_database_from_current_list_of_files():
    # global new_file_list_data
    new_file_list_data = create_a_list_of_file_information()
    write_to_audit_log_and_close(audit_log_full_file_name, "Creating new file list from current file")

    return new_file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def filter_out_the_file_database_file_from_the_list_of_files(temp_file_list_data) -> list:
    final_temp_file_list_data = []

    for entry in temp_file_list_data:
        if full_db_file_name in entry:
            pass
        else: 
            final_temp_file_list_data.append(entry)

    return final_temp_file_list_data
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  ### What is the file is unique

def merge_old_and_new_list_of_files(file_list_data_for_merge, new_file_list_data_for_merge):

    final_file_list_data = []
    temp_file_list_data = []
    temp_file_list_data2 = []

    # Concatinate the two files
    temp_file_list_data2 = file_list_data_for_merge + new_file_list_data_for_merge

    # Remove the database file from the list
    temp_file_list_data = filter_out_the_file_database_file_from_the_list_of_files(temp_file_list_data2)
    
    # Sort the file list using the file name (first entry in the list)
    temp_file_list_data.sort(key=lambda filename: filename[0])   

    # Compare two adjacent rows, if the filenames are the same, the keep the  one with the higher status
    # [0 = filename,  1 = size in bytes,  2 = status]
    number_of_entries_in_list = len(temp_file_list_data)
    previous_duplicate_entries = False
    for entry in range(0, number_of_entries_in_list-1):

        if (previous_duplicate_entries == False):  # skip processing if previous were the same
            print (f"-------------  previous_duplicate_entries {previous_duplicate_entries}")
            print (f"Current Entry: {entry:3.0f} {temp_file_list_data[entry]}")
            print (f"Next Entry:    {(entry+1):3.0f} {temp_file_list_data[entry+1]}")

            if (temp_file_list_data[entry][0] == temp_file_list_data[entry+1][0]):  
                
            # if this file and next file have the same name
                if int(temp_file_list_data[entry][2]) > int(temp_file_list_data[entry+1][2]):   # compare the status codes
                    final_file_list_data.append(temp_file_list_data[entry])                     # Keep the first file if the SC is higher
                    print  ("Same Kept first")
                else:
                    final_file_list_data.append(temp_file_list_data[entry+1])                   # Keeps the second file if the SC is higher
                    print ("Same Kept Second")
                previous_duplicate_entries = True
            else:
                final_file_list_data.append(temp_file_list_data[entry])   #### ADDED AND BROKE
                print (f"{entry:3.0f} Different Kept first") 
                previous_duplicate_entries = False
        else:
                previous_duplicate_entries = False



    return final_file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def transfer_files_to_server( filename_to_be_transferred : str, remote_filename = ""):
    # Replace with your own connection details
    hostname = '192.168.1.250'
    username = 'a'
    private_key_path = "/home/a/.ssh/id_rsa" 
    local_directory ='/home/a/vision_movement_files/'
    local_file_name = filename_to_be_transferred
    local_path = local_file_name
    remote_path = 'D:/Tree_video/'
    remote_path_filename = remote_path + remote_filename

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path) 

    def progress(filename, size, sent):
        sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100))
        sys.stdout.flush()

    try:
        # 1. Establish the SSH connection
        ssh_client.connect(hostname, username=username, pkey=private_key)
        print("SSH connection established.")

        # 2. Create an SCP client using the SSH transport
        with SCPClient(ssh_client.get_transport(), progress=progress) as scp:
            # 3. Transfer the file
            # print(f"Transferring {local_path} to {remote_path_filename}...")
            write_to_audit_log_and_close(audit_log_full_file_name, f"Transferring {local_path} to {remote_path_filename}...")
            scp.put(local_path, remote_path_filename)
            # print("File transfer successful.")
            write_to_audit_log_and_close(audit_log_full_file_name, f"File transfer successful.")
            # write_to_audit_log_and_close(audit_log_full_file_name, f".")
            

    except paramiko.ssh_exception.AuthenticationException as e:
        print(f"Authentication failed: {e}")
    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH connection error: {e}")
    except SCPException as e:
        print(f"SCP transfer failed: {e}")
    except FileNotFoundError:
        print(f"Local file not found: {local_path}")
    except socket.timeout:
        print("Connection timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # 4. Ensure the SSH connection is closed
        if ssh_client:
            ssh_client.close()
            print("SSH connection closed.")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def set_status_for_small_files(list_to_be_modified : list, size_threshold : int, status_code: int) -> list:
    for entry in list_to_be_modified:
        if ( int(entry[1]) < size_threshold ):
            entry[2] = status_code
    return list_to_be_modified

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def delete_files_marked_for_deletion(file_list : list):

    for entry in file_list:
        filename = entry[0]
        if (entry[2] == file_transfer_status.READY_FOR_DELETION):
            try:
                os.remove(filename)
                # print(f"File '{filename}' deleted successfully.")
                write_to_audit_log_and_close(audit_log_full_file_name, f"File '{filename}' deleted successfully.")
            except FileNotFoundError:
                print(f"File '{filename}' does not exist.")
            except OSError as e:
                print(f"Error deleting file '{filename}': {e}")
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def delete_database_file(file_list_data_file_DB  : str):

    filename = file_list_data_file_DB

    try:
        os.remove(filename)

        # print(f"File '{filename}' deleted successfully.")
        write_to_audit_log_and_close(audit_log_full_file_name, f"File '{filename}' deleted successfully.")
    except FileNotFoundError:
        write_to_audit_log_and_close(audit_log_full_file_name, f"File '{filename}' does not exist.")
    except OSError as e:
        print(f"Error deleting file '{filename}': {e}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def scp_files_marked_for_transfer(file_list : list) -> list:

    for entry in file_list:
        print (f"Entry {entry}")
        filename = entry[0]
        if (entry[2] == file_transfer_status.READY_FOR_TRANSFER):
            transfer_files_to_server(filename)
        entry[2] == file_transfer_status.TRANSFERRED
    return file_list

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def copy_file_transfer_status_to_server_with_time_stamp_in_filename():

    target_file_name = create_current_time_String() + "_" + file_list_data_file_DB
    transfer_files_to_server( file_list_data_file_DB, target_file_name)
    # print(f"Copying current status file to server with name {target_file_name}")
    write_to_audit_log_and_close(audit_log_full_file_name, f"Copying current status file to server with name {target_file_name}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def create_current_time_String() -> str:
    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%m_%d_%H_%M_%S")
    return formatted_date_time

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def review_the_age_of_new_files_and_update_to_ready_to_transfer(file_list : list) -> list:
    # Read the file name and calculate how old the file is. If greater than 130 minutes then mark ready for transfer

    age_in_minutes_threshold = 130

    now = datetime.now()    # Get the current date and time
    # Create a datetime object for the start of the current year (January 1st, 00:00:00)
    start_of_year = datetime(now.year, 1, 1, 0, 0, 0)

    # Calculate the time difference (timedelta)
    time_difference = now - start_of_year

    # Get the total number of seconds in the timedelta and convert to minutes
    minutes_since_start_of_year = time_difference.total_seconds() / 60

    for entry in file_list:

        # Get just the filename from the full path-file name  # /home/a/vision_movement_files/10_18_14_51_21_Movement.avi
        filename = entry[0].replace(video_log_directory_path, "")
        # print (f"Entry[0]  {filename}  entry[1]   {entry[1]}   entry[2] {entry[2]}")
        file_month  = int(filename[0:2])
        file_day    = int(filename[3:5])
        file_hour   = int(filename[6:8])
        file_minute = int(filename[9:11])

        time_object_file_creation = datetime(now.year, file_month, file_day, file_hour, file_minute)
        time_object_time_difference = time_object_file_creation - start_of_year
        year_minutes_of_file_creation  = time_object_time_difference.total_seconds() / 60
        age_of_file_minutes = minutes_since_start_of_year - year_minutes_of_file_creation
    
        # print(f" name: {filename} create_minutes: {year_minutes_of_file_creation} || current time minutes in year: {minutes_since_start_of_year:6.0f}  || age: {age_of_file_minutes:6.0f}   ")

        if (age_of_file_minutes > age_in_minutes_threshold):
            entry[2] = file_transfer_status.READY_FOR_TRANSFER
            print ("STATUS Setting ready to transfer")

    return file_list
    
    # Read the file name and calculate how old the file is. If greater than 130 minutes then mark ready for transfer

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def create_audit_log_file_name_based_on_time() -> str:
    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%m_%d_%H_%M_%S")
    audit_log_full_file_name = audit_log_file_path + formatted_date_time + "_audit_log.txt"
    return audit_log_full_file_name

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def write_to_audit_log_and_close(audit_log_full_file_name, comment_to_add):
    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%m_%d_%H_%M_%S")
    comment = "\n" + formatted_date_time + " " + comment_to_add
    with open(audit_log_full_file_name, "a") as file:
        file.write(comment)
    print (comment)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def main():

    number_of_loops = 5
    pause_seconds = 30
    global audit_log_full_file_name
    audit_log_full_file_name = create_audit_log_file_name_based_on_time()

    file_list_data = get_existing_database_or_create_new_one()
    # print_list_of_file_information_to_screen(file_list_data, "After pulling or creating first DB")

    for counter in range(number_of_loops):

        new_file_list_data = create_new_database_from_current_list_of_files()
        print_list_of_file_information_to_screen(new_file_list_data, "After creating fresh DB")
        
        updated_file_list_data = merge_old_and_new_list_of_files(file_list_data, new_file_list_data)
        print_list_of_file_information_to_screen(updated_file_list_data, "Final Merged List")

        # - Remove small files
        updated_file_list_2 = set_status_for_small_files(updated_file_list_data, 6000, file_transfer_status.READY_FOR_DELETION)
        # print_list_of_file_information_to_screen(updated_file_list_2, "Marked small files")

        # - Delete files
        delete_files_marked_for_deletion(updated_file_list_2)

        # HOW TO TRANSITION FROM new TO ready to transfer
        # Read the file name and calculate how old the file is. If greater than 130 minutes then mark ready for transfer
        updated_file_list_3 = review_the_age_of_new_files_and_update_to_ready_to_transfer(updated_file_list_2)

        print_list_of_file_information_to_screen(updated_file_list_3, "Mark ready to tranfer")

        # - Copy current files over and update status 
        updated_file_list_5 = scp_files_marked_for_transfer(updated_file_list_3)

        print_list_of_file_information_to_screen(updated_file_list_5, "After  transferred ")

        copy_file_transfer_status_to_server_with_time_stamp_in_filename()

        
        write_to_audit_log_and_close(audit_log_full_file_name, f"Pausing {pause_seconds}")
        time.sleep(pause_seconds)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


# class file_transfer_status():
#    NEW                = 1   - File just created.  May not be complete
#    READY_FOR_TRANSFER = 2   - Waited at least two hours after creation time
#    TRANSFERRED        = 3   - Transfer complete
#    READY_FOR_DELETION = 4   - Set this code once transfer is complete or file is too small
#    DELETED            = 5   - Set this code once transfer is complete or file is too small

#  If this program is run every 4 hours
# 
#  When should I delete the status file?
#   Never?
#   Startup?

# Should I periodically copy the status file to the server with a date-time stamp?

# Should I periodically list the contents of the status file?