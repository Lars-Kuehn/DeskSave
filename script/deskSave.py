import os
import getpass
import datetime
import json
import shutil

def load_file_types():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'file_types.json')
    
    # Open and load the JSON file
    with open(json_path, 'r') as file:
        return json.load(file)

def move_files(source, destination, file_types, skip_files, skip_folders):
    # Ensure the destination path exists
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    # Only process files and folders in the root of the source directory (no recursive walk)
    for item in os.listdir(source):
        full_path = os.path.join(source, item)
        
        # Skip folders in skip_folders list
        if os.path.isdir(full_path) and item in skip_folders:
            print(f"Skipping folder: {item}")
            continue
        
        # Skip files in skip_files list or hidden files
        if item in skip_files or item.startswith('.'):
            print(f"Skipping file: {item}")
            continue
        
        # If it's a folder, move it as well
        if os.path.isdir(full_path):
            # Normalize folder name and create corresponding destination folder
            folder_dest = os.path.join(destination, item)
            if not os.path.exists(folder_dest):
                os.makedirs(folder_dest)
            
            # Move all contents inside the folder to the corresponding destination folder
            for sub_item in os.listdir(full_path):
                sub_item_path = os.path.join(full_path, sub_item)
                shutil.move(sub_item_path, os.path.join(folder_dest, sub_item))
                print(f"Moved: {sub_item} to {folder_dest}")
            
            # After moving the contents, delete the empty source folder
            try:
                os.rmdir(full_path)  # Removes the folder if it's empty
                print(f"Deleted empty folder: {item}")
            except OSError:
                print(f"Failed to delete folder {item} (it may not be empty)")

        # If it's a file, proceed to check extension and organize
        elif os.path.isfile(full_path):
            # Normalize the file extension to lowercase
            file_extension = item.split('.')[-1].lower()
            
            # Determine file type category and move accordingly
            for file_type, data in file_types.items():
                if file_extension in [ext.lower() for ext in data["extensions"]]:  # Convert JSON extensions to lowercase
                    # Define the destination directory based on file type and source folder name
                    file_type_dest = os.path.join(destination, file_type)
                    if not os.path.exists(file_type_dest):
                        os.makedirs(file_type_dest)
                    
                    # Move the file
                    shutil.move(full_path, os.path.join(file_type_dest, item))
                    print(f"Moved: {item} to {file_type_dest}")
                    break  # Exit loop once file is moved

if __name__ == '__main__':
    # Define the allowed source folders
    user = getpass.getuser()
    allowed_sources = {
        'Desktop': f'/Users/{user}/Desktop',
        'Downloads': f'/Users/{user}/Downloads'
    }
    
    # Prompt the user to choose between Desktop and Downloads
    print("Choose source folder to organize:")
    print("1. Desktop")
    print("2. Downloads")
    choice = input("Enter 1 or 2: ").strip()
    
    # Set the source based on user's choice
    if choice == '1':
        source = allowed_sources['Desktop']
        source_folder_name = "Desktop"
    elif choice == '2':
        source = allowed_sources['Downloads']
        source_folder_name = "Downloads"
    else:
        print("Invalid choice. Exiting.")
        exit(1)
    
    # Get the current date to create a unique destination folder
    date = datetime.datetime.today().strftime("%Y-%m")
    
    # Set the destination directory, creating a subfolder based on the chosen source folder
    destination = f'/Users/{user}/Documents/OrganizedFiles/{date}/{source_folder_name}/'
    
    # Load file type data from JSON
    file_types = load_file_types()
    
    # Define lists of files and folders to skip
    skip_files = ['.DS_Store', 'README.md']  # Add more file names or extensions as needed
    skip_folders = ['DeskSave', 'Downloads', 'Documents']  # Add more folder names as needed
    
    # Move files and folders based on type, skipping specified files and folders
    move_files(source, destination, file_types, skip_files, skip_folders)
    print("Organizing complete.")