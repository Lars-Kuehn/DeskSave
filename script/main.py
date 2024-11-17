""" This module contains all the logic involving the DeskSave GUI and Algorithm"""

import os
import getpass
import datetime
import json
import shutil
import sys
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

class DeskSaveApp(tk.Tk): # pylint: disable=too-many-instance-attributes
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
        super().__init__()
        self.title("DeskSave")
        self.configure(bg="#1e1e1e")
        self.geometry("600x400")

        # Initialize the default JSON configuration path
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_json_path = os.path.join(self.script_dir, 'file_types.json')
        self.custom_json_path = None  # Holds the path to the custom JSON file if uploaded

        # Load file types
        self.file_types = self.load_file_types()

        # Set up source options
        self.user = getpass.getuser()
        self.allowed_sources = {
            'Desktop': f'/Users/{self.user}/Desktop',
            'Downloads': f'/Users/{self.user}/Downloads'
        }

        # Create Menus
        self.create_menus()

        # Set up GUI
        self.create_widgets()

    def create_menus(self):
        """
        Creates the main menu bar with cascading submenus.
        """
        menu_bar = tk.Menu(self)

        # Settings Menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        
        # Config Submenu
        config_menu = tk.Menu(settings_menu, tearoff=0)
        config_menu.add_command(label="Upload Custom Config", command=self.upload_custom_config)
        config_menu.add_command(label="Remove Custom Config", command=self.remove_custom_config)
        config_menu.add_command(label="About Config Syntax", command=self.about_custom_config)

        # Add Config submenu to Settings
        settings_menu.add_cascade(label="Config", menu=config_menu)

        # Add Settings to Menu Bar
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # About Menu
        menu_bar.add_command(label="About", command=self.show_about)

                # About Menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About DeskSave", command=self.show_about)
        menu_bar.add_cascade(label="About", menu=about_menu)

        # Attach Menu Bar to the App
        self.config(menu=menu_bar)


    def upload_custom_config(self):
        """
        Allows the user to upload a custom JSON file for file type configuration.
        The uploaded file will be used instead of the default configuration.
        """
        # Prompt the user to select a JSON file
        file_path = filedialog.askopenfilename(
            title="Select a JSON Configuration File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                # Validate the JSON format
                with open(file_path, 'r', encoding='UTF-8') as new_file:
                    new_config = json.load(new_file)

                # Set the custom JSON file as the active configuration
                self.custom_json_path = file_path
                self.file_types = new_config
                messagebox.showinfo("Preferences", "Custom configuration loaded successfully!")

            except json.JSONDecodeError:
                messagebox.showerror("Invalid File", "The selected file is not a valid JSON configuration.")
            except Exception as e: # pylint: disable=broad-exception-caught
                messagebox.showerror("Error", f"An error occurred: {e}")

    def remove_custom_config(self):
        """
        Removes the custom configuration and reverts to the default JSON configuration.
        """
        if self.custom_json_path:
            self.custom_json_path = None
            self.file_types = self.load_file_types()
            messagebox.showinfo("Preferences", "Reverted to the default configuration.")
        else:
            messagebox.showinfo("Preferences", "No custom configuration to remove.")

    def about_custom_config(self):
        """
        Displays information about the syntax of the JSON configuration file in a formatted way,
        along with an explanation of each field's purpose, using a custom Toplevel window.
        """
        json_example = {
            "Images": {"extensions": ["jpg", "png", "gif"]},
            "Documents": {"extensions": ["pdf", "docx", "txt"]},
            "Videos": {"extensions": ["mp4", "mkv", "avi"]},
        }

        formatted_json = json.dumps(json_example, indent=4)

        explanation = (
            "Explanation of JSON fields:\n\n"
            "1. Each top-level key (e.g., 'Images', 'Documents') represents a category. This category also represents the folder name.\n"
            "2. Under each category, the 'extensions' field specifies a list of file extensions that belong to that category.\n"
            "3. The extensions should not include the leading dot (e.g., 'jpg' not '.jpg').\n\n"
            "The application uses this configuration to sort files into the specified categories."
        )

        # Create a Toplevel window
        about_window = tk.Toplevel(self)
        about_window.title("About Config")
        about_window.geometry("600x500")
        about_window.configure(bg="#1e1e1e")

        # Title Label
        title_label = tk.Label(
            about_window,
            text="Configuration File Syntax",
            font=("Arial", 16),
            fg="#1e90ff",
            bg="#1e1e1e"
        )
        title_label.pack(pady=10)

        # Text widget to display JSON and explanation
        text_area = tk.Text(about_window, wrap=tk.WORD, bg="#252526", fg="white", font=("Courier", 12))
        text_area.insert(tk.END, "The configuration file should follow this syntax:\n\n")
        text_area.insert(tk.END, formatted_json + "\n\n")
        text_area.insert(tk.END, explanation)
        text_area.config(state=tk.DISABLED)  # Make the text area read-only
        text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Close button
        close_button = tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            bg="#1e90ff",
            fg="black",
            font=("Arial", 12)
        )
        close_button.pack(pady=10)

    def show_about(self):
        """
        Displays information about the application, including its version.
        """
        app_version = os.getenv("APP_VERSION", "NO-STABLE-RELEASE")
        messagebox.showinfo(
            "About DeskSave",
            f"DeskSave {app_version}\n\nAn application to organize your files effortlessly!"
        )

    def load_file_types(self):
        """
        Loads file type configurations from the active JSON configuration file.
        If a custom JSON file is not provided, it defaults to the original 'file_types.json'.

        Returns:
            dict: A dictionary where keys represent file type categories (e.g., 'Images', 
            'Documents') and values are lists of associated file extensions.

        Raises:
            SystemExit: If the active configuration file is missing or has an invalid format.
        """
        active_path = self.custom_json_path or self.default_json_path
        try:
            with open(active_path, 'r', encoding='UTF-8') as file:
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
    app = DeskSaveApp()
    app.mainloop()
