import os
import csv

class file_transfer_status():
   NEW = 1
   READY_FOR_TRANSFER = 2
   TRANSFERRED = 3
   READY_FOR_DELETION = 4
   DELETED = 5

video_log_directory_path = "/home/a/vision_movement_files/"  
file_list_data_file_DB = "file_list_data_file_DB.txt"
full_db_file_name = video_log_directory_path + file_list_data_file_DB
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

    except FileNotFoundError:
        print("Data file not found. - Creating new database")

        file_list_data = create_a_list_of_file_information()
        write_list_of_file_information_to_disk(file_list_data)

    return file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def create_new_database_from_current_list_of_files():
    # global new_file_list_data
    new_file_list_data = create_a_list_of_file_information()
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

    for entry in range(0, number_of_entries_in_list-1):
        if (temp_file_list_data[entry][0] == temp_file_list_data[entry+1][0]):
            if int(temp_file_list_data[entry][2]) > int(temp_file_list_data[entry+1][2]):
                final_file_list_data.append(temp_file_list_data[entry])
            else:
                final_file_list_data.append(temp_file_list_data[entry+1])

    return final_file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def main():
    file_list_data = get_existing_database_or_create_new_one()
    # print_list_of_file_information_to_screen(file_list_data, "After pulling or creating first DB")

    new_file_list_data = create_new_database_from_current_list_of_files()
    # print_list_of_file_information_to_screen(new_file_list_data, "After creating fresh DB")
    
    updated_file_list_data = merge_old_and_new_list_of_files(file_list_data, new_file_list_data)
    print_list_of_file_information_to_screen(updated_file_list_data, "Final Merged List")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
