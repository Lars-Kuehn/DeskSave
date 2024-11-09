import os
import getpass
import datetime
import json
import shutil
import sys
import tkinter as tk
from tkinter import messagebox, ttk

class DeskSaveApp(tk.Tk):
    """
    DeskSaveApp is a Tkinter-based graphical user interface application for organizing 
    files by moving them from specified source folders (Desktop or Downloads) to 
    categorized directories based on file types within the user's Documents folder.

    This application loads a configuration of file types from a JSON file and provides 
    options for the user to select the source directory and initiate the file 
    organization process. It uses a dark theme with blue accents for visual styling.

    Attributes:
        file_types (dict): A dictionary of file type categories and their associated 
            file extensions, loaded from 'file_types.json'.
        user (str): The current user's username, used to determine source and 
            destination directories.
        allowed_sources (dict): A dictionary of allowed source directories 
            (Desktop and Downloads) specific to the user.
    """
    def __init__(self):
        """
        Initializes the DeskSaveApp GUI application. Sets up the main window's 
        appearance, loads file type configurations, defines the allowed source 
        directories for the current user, and initializes the GUI widgets.
        
        Raises:
            SystemExit: If the file type configuration file cannot be loaded due 
            to being missing or incorrectly formatted.
        """
        super().__init__()
        self.title("DeskSave")
        self.configure(bg="#1e1e1e")
        self.geometry("600x400")
        
        # Load file types
        self.file_types = self.load_file_types()
        
        # Set up source options
        self.user = getpass.getuser()
        self.allowed_sources = {
            'Desktop': f'/Users/{self.user}/Desktop',
            'Downloads': f'/Users/{self.user}/Downloads'
        }
        
        # Set up GUI
        self.create_widgets()
    
    def load_file_types(self):
        """
        Loads file type configurations from 'file_types.json' located in the same 
        directory as the script. The JSON file should contain a dictionary that maps 
        file type categories to their associated file extensions, which is used to 
        organize files by type in the application.

        Returns:
            dict: A dictionary where keys represent file type categories (e.g., 'Images', 
            'Documents') and values are lists of associated file extensions.

        Raises:
            SystemExit: If 'file_types.json' is missing or has an invalid JSON format. 
                Displays an error message to the user before exiting.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(script_dir, 'file_types.json')
            logging.info(f"Loading file types from: {json_path}")
            print(f"Loading file types from: {json_path}")
            with open(json_path, 'r', encoding='UTF-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Failed to load file types configuration.")
            sys.exit()
    
    def create_widgets(self):
        """
        Creates and arranges the graphical user interface (GUI) components for the DeskSaveApp.

        This includes setting up labels, dropdowns, buttons, and a text area to display
        progress. The GUI components allow the user to select a source folder, start
        the file organization process, and view a log of actions taken during execution.

        Components:
            - Title label displaying the application name.
            - Dropdown menu for selecting the source folder (Desktop or Downloads).
            - Organize button to initiate the file organization.
            - Progress text area to show real-time updates on files being moved or skipped.
        """
        # Title Label
        title_label = tk.Label(self, text="DeskSave", font=("Arial", 24), fg="#1e90ff", bg="#1e1e1e")
        title_label.pack(pady=20)
        
        # Source Selection
        source_label = tk.Label(self, text="Choose source folder to organize:", fg="white", bg="#1e1e1e")
        source_label.pack()
        
        # Dropdown for source selection
        self.source_var = tk.StringVar(value="Desktop")
        source_menu = ttk.Combobox(self, textvariable=self.source_var, values=list(self.allowed_sources.keys()), state="readonly")
        source_menu.pack(pady=10)
        
        # Organize Button
        organize_button = tk.Button(self, text="Organize Files", command=self.organize_files, bg="#1e90ff", fg="black", font=("Arial", 14))
        organize_button.pack(pady=20)
        
        # Progress Display
        self.progress_text = tk.Text(self, width=70, height=10, bg="#252526", fg="white", state="disabled")
        self.progress_text.pack(pady=10)
        
    def log_progress(self, message):
        """
        Logs a message to the progress text area within the GUI.

        Args:
            message (str): The message to display in the progress text area.
        
        Side Effects:
            Updates the progress text area with the provided message, automatically
            scrolling to the latest entry.
        """
        self.progress_text.config(state="normal")
        self.progress_text.insert(tk.END, f"{message}\n")
        self.progress_text.config(state="disabled")
        self.progress_text.see(tk.END)
        
    def organize_files(self):
        """
        Handles the file organization process based on the selected source folder.

        This method retrieves the user's choice from the dropdown menu, constructs a
        destination path within the user's Documents folder, and defines files and
        folders to skip. Then, it calls `move_files` to categorize and move files
        according to the loaded file type configurations.

        Side Effects:
            - Displays progress messages in the text area.
            - Shows an information dialog box upon completion.
        """
        choice = self.source_var.get()
        source = self.allowed_sources[choice]
        
        date = datetime.datetime.today().strftime("%Y-%m")
        destination = f'/Users/{self.user}/Documents/OrganizedFiles/{date}/{choice}/'
        
        skip_files = ['.DS_Store', 'README.md']
        skip_folders = ['DeskSave', 'Downloads', 'Documents']
        
        self.move_files(source, destination, self.file_types, skip_files, skip_folders)
        self.log_progress("Organizing complete.")
        messagebox.showinfo("Completed", "Organizing complete.")
    
    def move_files(self, source, destination, file_types, skip_files, skip_folders):
        """
        Moves and organizes files from the source directory to the destination directory,
        categorizing them based on their file types and the configuration specified in
        'file_types.json'.

        Files and folders can be excluded from the organization process based on the
        `skip_files` and `skip_folders` lists. After moving files, it attempts to delete
        any empty folders left in the source directory.

        Args:
            source (str): The directory to move files from.
            destination (str): The directory to move files to, with subdirectories
                organized by file type.
            file_types (dict): A dictionary that maps file types to their extensions.
            skip_files (list): List of file names or extensions to skip.
            skip_folders (list): List of folder names to skip.

        Side Effects:
            - Creates destination folders if they do not already exist.
            - Moves files and deletes empty folders in the source directory.
            - Logs progress messages to the GUI text area.
        
        Raises:
            OSError: If unable to delete an empty folder, logs an error message but
            continues the process for other files and folders.
        """
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        for item in os.listdir(source):
            full_path = os.path.join(source, item)
            
            if os.path.isdir(full_path) and item in skip_folders:
                self.log_progress(f"Skipping folder: {item}")
                continue
            if item in skip_files or item.startswith('.'):
                self.log_progress(f"Skipping file: {item}")
                continue
            
            if os.path.isdir(full_path):
                folder_dest = os.path.join(destination, item)
                if not os.path.exists(folder_dest):
                    os.makedirs(folder_dest)
                for sub_item in os.listdir(full_path):
                    sub_item_path = os.path.join(full_path, sub_item)
                    shutil.move(sub_item_path, os.path.join(folder_dest, sub_item))
                    self.log_progress(f"Moved: {sub_item} to {folder_dest}")
                
                try:
                    os.rmdir(full_path)
                    self.log_progress(f"Deleted empty folder: {item}")
                except OSError:
                    self.log_progress(f"Failed to delete folder {item} (it may not be empty)")
            elif os.path.isfile(full_path):
                file_extension = item.split('.')[-1].lower()
                for file_type, data in file_types.items():
                    if file_extension in [ext.lower() for ext in data["extensions"]]:
                        file_type_dest = os.path.join(destination, file_type)
                        if not os.path.exists(file_type_dest):
                            os.makedirs(file_type_dest)
                        shutil.move(full_path, os.path.join(file_type_dest, item))
                        self.log_progress(f"Moved: {item} to {file_type_dest}")
                        break

if __name__ == '__main__':
    import sys
    import logging

    # Set up logging to a file
    log_file = "app_log.txt"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(message)s')

    # Redirect print statements to the log file
    sys.stdout = open(log_file, 'a')
    sys.stderr = sys.stdout  # Optional, redirect stderr to the same file

    app = DeskSaveApp()
    app.mainloop()
