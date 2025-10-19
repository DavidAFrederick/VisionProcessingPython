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

# List all files and directories
all_entries = sorted(os.listdir(video_log_directory_path))
file_status = file_transfer_status.NEW

for entry in all_entries:
    full_entry_name = video_log_directory_path + entry
    file_size_bytes = os.path.getsize(full_entry_name)
    file_list_data.append([full_entry_name, file_size_bytes, file_status])

for row in file_list_data:
    print (f"Row:  |{row}| ")


with open(full_db_file_name, "w") as file:
    for item in file_list_data:
        file.write(str(item) + "\n")

with open(full_db_file_name, 'r') as file:
    all_lines_of_data = file.readlines()
    file_list_data2 = [line.strip() for line in all_lines_of_data]

for row in file_list_data2:
    print (f"Row2:  |{row}| ")


