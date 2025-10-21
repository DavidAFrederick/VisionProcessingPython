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
    print(f"Creating new List of File Information by reading entries from the disk")
    new_file_list_data =[]
    all_entries = sorted(os.listdir(video_log_directory_path))
    file_status = file_transfer_status.NEW

    for entry in all_entries:
        full_entry_name = video_log_directory_path + entry
        file_size_bytes = os.path.getsize(full_entry_name)
        new_file_list_data.append([full_entry_name, file_size_bytes, file_status])

    print (f"{len(file_list_data)} Row created in List    (create_a_list_of_file_information)")
    return new_file_list_data

# #---------------------------------------------------------------------------------------------

def print_list_of_file_information_to_screen(file_list_data_to_print : list, note : str):
    # global file_list_data
    print("----------------------------------------------------")
    print (file_list_data_to_print)
    print(f" file_list_data_to_print [0][0]  {file_list_data_to_print [0][0] }")
    print(f" file_list_data_to_print [0][1]  {file_list_data_to_print [0][1] }")
    print(f" file_list_data_to_print [0][2]  {file_list_data_to_print [0][2] }")
    print(f" file_list_data_to_print [1][0]  {file_list_data_to_print [1][0] }")
    print(f" file_list_data_to_print [1][1]  {file_list_data_to_print [1][1] }")
    print(f" file_list_data_to_print [1][2]  {file_list_data_to_print [1][2] }")

    if (file_list_data_to_print != None):
        print (f"NOTE: {note}     Number Rows: {len(file_list_data_to_print)}")
        for row_of_data in file_list_data_to_print:
            print (f"{row_of_data}     {note}")
    else:
        print(f"NOTE: {note}  The list is empty")

# #---------------------------------------------------------------------------------------------
def write_list_of_file_information_to_disk(file_list_data_to_disk : list):
    # global file_list_data

    # with open(full_db_file_name, "w") as file:
    #     for item in file_list_data_to_disk:
    #         file.write(str(item) + "\n")

    # Write the list of lists to a CSV file
    with open(full_db_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(file_list_data_to_disk)

# #---------------------------------------------------------------------------------------------
def read_list_of_file_information_from_disk() -> list:
    # global file_list_data

    # with open(full_db_file_name, 'r') as file:
    #     all_lines_of_data = file.readlines()
    #     file_list_data = [line.strip() for line in all_lines_of_data]

    # with open(full_db_file_name, 'r') as file:
    #     all_lines_of_data = file.readlines()
    #     file_list_data = [line.strip() for line in all_lines_of_data]

    # print (f"READING LIST FROM DISK")
    # file_list_data = []
    # with open(full_db_file_name, 'r') as file:
    #     for line in file:
    #         # Remove leading/trailing whitespace and split the line by the delimiter
    #         # inner_list = line.strip().split(",")
    #         # print(f"Inner List {inner_list}")
    #         # file_list_data.append(inner_list)
    #         line2 = line.strip('"')
    #         line3 = line2.strip('\n')
    #         print(f"line2   {line2}")
    #         print(f"line3   {line3}")
    #         entry_list = []

    #         file_list_data.append(line3)
    #         print (file_list_data)

    # Read the CSV file back into a list of lists

    print (f"READING LIST FROM DISK")
    file_list_data = []
    
    with open(full_db_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            file_list_data.append(row)

    print_list_of_file_information_to_screen(file_list_data, "CREATING NEW LIST from DISK")

    print (f"{len(file_list_data)} rows of in List read from the disk")
    return file_list_data

# THIS IS NOT WORKING CORRECTLY, NOT CREATING A  LIST of LISTS

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_existing_database_or_create_new_one():
    global file_list_data
    try:
        file_list_data = read_list_of_file_information_from_disk()
        print_list_of_file_information_to_screen(file_list_data, "TRY creating new list")

    except FileNotFoundError:
        print("Data file not found. - Creating new database")

        file_list_data = create_a_list_of_file_information()
        print_list_of_file_information_to_screen(file_list_data, "EXCEPTION creating new list")
        write_list_of_file_information_to_disk(file_list_data)

    # else:
    #     print_list_of_file_information_to_screen(file_list_data, "ELSE")
    #     #  UNDER WHAT CONDITIONS IS THIS CALLED?

    # finally:
    #     print("File operation attempt completed.")

    return file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def create_new_database_from_current_list_of_files():
    # global new_file_list_data
    new_file_list_data = create_a_list_of_file_information()
    return new_file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def merge_old_and_new_list_of_files(file_list_data_for_merge, new_file_list_data_for_merge):
    # global file_list_data, new_file_list_data



    print_list_of_file_information_to_screen(file_list_data_for_merge, " 1  merge_old_and_new_list_of_files")
    print_list_of_file_information_to_screen(new_file_list_data_for_merge, " 2  merge_old_and_new_list_of_files")

    final_file_list_data = []
    temp_file_list_data = []
    temp_file_list_data2 = []
    temp_file_list_data = file_list_data_for_merge + new_file_list_data_for_merge
    print_list_of_file_information_to_screen(temp_file_list_data, ">> two file appended ")

    found = False
    for entry in temp_file_list_data:
        if full_db_file_name in entry:
            print(f"FOUND: >{file_list_data_file_DB}<   >{entry}<")
        else: 
            print(f"Not Found appending {entry}")
            temp_file_list_data2.append(entry)

    temp_file_list_data = temp_file_list_data2
    
    temp_file_list_data.sort(key=lambda filename: filename[0])   
    # temp_file_list_data2 = temp_file_list_data.sort()  # ERROR ON SORTING
    # temp_file_list_data2 = sorted(temp_file_list_data, key=lambda x: x[0])
    print_list_of_file_information_to_screen(temp_file_list_data, ">> AFTER sorted")

    number_of_entries_in_list = len(temp_file_list_data)

    for entry in range(0, number_of_entries_in_list-1):
        if (temp_file_list_data[entry][0] == temp_file_list_data[entry+1][0]):
            if int(temp_file_list_data[entry][2]) > int(temp_file_list_data[entry+1][2]):
                final_file_list_data.append(temp_file_list_data[entry])
            else:
                final_file_list_data.append(temp_file_list_data[entry+1])


    for entry in final_file_list_data:
        print(f"Final combined list: {entry}")

    print("4===============================================")
    return final_file_list_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def main():
    file_list_data = get_existing_database_or_create_new_one()
    print_list_of_file_information_to_screen(file_list_data, "After pulling or creating first DB")

    new_file_list_data = create_new_database_from_current_list_of_files()
    print_list_of_file_information_to_screen(new_file_list_data, "After creating fresh DB")
    updated_file_list_data = merge_old_and_new_list_of_files(file_list_data, new_file_list_data)
    print_list_of_file_information_to_screen(updated_file_list_data, "Final Merged List")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
