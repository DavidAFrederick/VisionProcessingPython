import os

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

# #---------------------------------------------------------------------------------------------
def create_a_list_of_file_information():
    # List all files and directories
    print(f"Creating new List of File Information")
    all_entries = sorted(os.listdir(video_log_directory_path))
    file_status = file_transfer_status.NEW

    for entry in all_entries:
        full_entry_name = video_log_directory_path + entry
        file_size_bytes = os.path.getsize(full_entry_name)
        file_list_data.append([full_entry_name, file_size_bytes, file_status])

    print (f"{len(file_list_data)} Row created in List")

# #---------------------------------------------------------------------------------------------

def print_list_of_file_information_to_screen():
    for row_of_data in file_list_data:
        print (f"{row_of_data}")

# #---------------------------------------------------------------------------------------------
def write_list_of_file_information_to_disk():
    with open(full_db_file_name, "w") as file:
        for item in file_list_data:
            file.write(str(item) + "\n")

# #---------------------------------------------------------------------------------------------
def read_list_of_file_information_from_disk():
    with open(full_db_file_name, 'r') as file:
        all_lines_of_data = file.readlines()
        file_list_data = [line.strip() for line in all_lines_of_data]

    print (f"{len(file_list_data)} rows of in List")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_existing_database_or_create_new_one():
    try:
        read_list_of_file_information_from_disk()
        print ("Existing List of Data found on Disk")

    except FileNotFoundError:
        print("Data file not found. - Creating new database")

        create_a_list_of_file_information()
        print_list_of_file_information_to_screen()
        write_list_of_file_information_to_disk()

    else:
        print_list_of_file_information_to_screen()

    finally:
        print("File operation attempt completed.")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def main():
    get_existing_database_or_create_new_one()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
