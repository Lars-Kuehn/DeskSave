"""DeskSave Module""" # pylint: disable=too-many-lines

import os
import getpass
import datetime
import json
import shutil
import sys
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import pyperclip

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
        # Color Palette
        # Color Palette
        self.background = "#040D12"  # Dark background
        self.boxes = "#183D3D"  # Widget background
        self.menu = "#5C8374"  # Menu and button accents
        self.text = "#EEEEEE"  # Primary text color

        # App Configuration
        self.title("DeskSave")
        self.configure(bg=self.background)
        self.geometry("800x600")

        # Initialize the default JSON configuration path
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_json_path = os.path.join(self.script_dir, 'file_types.json')
        self.default_ignore_json_path = os.path.join(self.script_dir, 'ignore.json')
        self.custom_json_path = None  # Holds the path to the custom JSON file if uploaded

        # Load file types
        self.file_types = self.load_file_types()

        # Set up source options
        self.user = getpass.getuser()
        self.allowed_sources = { # Default sources
            'Desktop': f'/Users/{self.user}/Desktop',
            'Downloads': f'/Users/{self.user}/Downloads'
        }

        # Initalize Ignoring of Files and Folders
        self.ignore_files, self.ignore_folders = self.load_ignore_json()

        # Initialize custom destination path
        self.custom_destination_path = None

        # Get the current month and year for the default destination path
        self.current_month_year = datetime.now().strftime("%m-%Y")

        # Set the default destination path to be inside the user's Documents/DeskSave folder, with the month-year subfolder
        self.default_destination_path = os.path.join(f'/Users/{self.user}/Documents', 'DeskSave', self.current_month_year)

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
        config_menu.add_command(label="Config Syntax", command=self.syntax_config)
        config_menu.add_command(label="About Config", command=self.about_config)

        # Path Submenu
        path_menu = tk.Menu(settings_menu, tearoff=0)
        path_menu.add_command(label="Add Source-Path", command=self.add_custom_source)
        path_menu.add_command(label="Change Destination-Path", command=self.change_destination)
        path_menu.add_command(label="About Changing Paths", command=self.about_paths)

        # Ignore Submenu
        ignore_menu = tk.Menu(settings_menu, tearoff=0)
        ignore_menu.add_command(label="Ignore Files & Folders", command=self.ignore_data)
        ignore_menu.add_command(label="About Ignoring", command=self.about_ignoring)

        # Add Submenus to Settings
        settings_menu.add_cascade(label="File Configuration", menu=config_menu)
        settings_menu.add_cascade(label="Path Configuration", menu=path_menu)
        settings_menu.add_cascade(label="Ignore Configuration", menu=ignore_menu)

        # Add Settings to Menu Bar
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # About Menu
        menu_bar.add_command(label="About", command=self.show_about)

        # Attach Menu Bar to the App
        self.config(menu=menu_bar)

    #
    # CUSTOM CONFIG
    #

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

    def syntax_config(self):
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
            "1. Each top-level key (e.g., 'Images', 'Documents') represents a category.\n"
            "   This category also represents the folder name.\n"
            "2. Under each category, the 'extensions' field specifies a list of file extensions\n"
            "   that belong to that category.\n"
            "3. The extensions should not include the leading dot (e.g., 'jpg' not '.jpg').\n\n"
            "The application uses this configuration to sort files into the specified categories."
        )

        # Create a Toplevel window
        about_window = tk.Toplevel(self)
        about_window.title("Configuration File Syntax")
        about_window.geometry("700x900")
        about_window.configure(bg=self.background, padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            about_window,
            text="Configuration File Syntax",
            font=("Helvetica", 18, "bold"),
            fg=self.text,
            bg=self.boxes,
            padx=10,
            pady=10,
            relief=tk.RIDGE
        )
        title_label.pack(pady=(10, 20))

        # Frame for JSON example
        json_frame = tk.Frame(about_window, bg=self.boxes, relief=tk.GROOVE, bd=2)
        json_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label for JSON syntax
        json_label = tk.Label(
            json_frame,
            text="JSON Syntax Example:",
            font=("Helvetica", 14, "bold"),
            fg="#4CAF50",  # Green text
            bg=self.boxes,
            anchor="w"
        )
        json_label.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Text widget to display JSON
        json_text_area = tk.Text(
            json_frame, wrap=tk.WORD, bg="#F5F5F5", fg="#212121", font=("Courier", 12), height=12
        )
        json_text_area.insert(tk.END, formatted_json)
        json_text_area.config(state=tk.DISABLED)  # Make it read-only
        json_text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Copy to Clipboard button
        copy_button = tk.Button(
            json_frame,
            text="Copy JSON to Clipboard",
            command=lambda: pyperclip.copy(formatted_json),
            bg="#4CAF50",  # Green
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        copy_button.pack(pady=10)

        # Explanation Label
        explanation_frame = tk.Frame(about_window, bg=self.background)
        explanation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        explanation_label = tk.Label(
            explanation_frame,
            text="Explanation of Configuration:",
            font=("Helvetica", 14, "bold"),
            fg="#F57C00",  # Orange text
            bg=self.background,
            anchor="w"
        )
        explanation_label.pack(fill=tk.X, pady=(10, 5))

        explanation_text_area = tk.Text(
            explanation_frame, wrap=tk.WORD, bg=self.boxes, fg=self.text, font=("Arial", 12), height=8
        )
        explanation_text_area.insert(tk.END, explanation)
        explanation_text_area.config(state=tk.DISABLED)  # Make it read-only
        explanation_text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Close button
        close_button = tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            bg="#B71C1C",  # Red
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        close_button.pack(pady=(10, 20))

    def about_config(self):
        """
        Displays information about uploading a custom config with a more engaging and visually appealing UI.
        """
        # Create a new Toplevel window
        about_window = tk.Toplevel(self)
        about_window.title("About Uploading Configurations")
        about_window.geometry("550x600")
        about_window.configure(bg=self.background, padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            about_window,
            text="Uploading a Custom Configuration",
            font=("Helvetica", 18, "bold"),
            fg="#4CAF50",  # Green color for emphasis
            bg=self.background
        )
        title_label.pack(pady=(10, 20))

        # Explanation Text
        explanation = (
            "You can upload your own configuration file to specify how files "
            "should be sorted into categories. Follow the steps below to ensure "
            "the configuration is correct."
        )

        explanation_label = tk.Label(
            about_window,
            text=explanation,
            font=("Arial", 12),
            fg=self.text,
            bg=self.background,
            wraplength=500,
            justify=tk.LEFT,
            anchor="nw"
        )
        explanation_label.pack(pady=(5, 15), fill=tk.BOTH)

        # Instructions Section
        instructions_label = tk.Label(
            about_window,
            text="Instructions:",
            font=("Arial", 14, "bold"),
            fg="#F57C00",  # Orange to highlight the instructions
            bg=self.background,
            anchor="w"
        )
        instructions_label.pack(fill=tk.X, pady=(10, 5))

        # Instruction Steps
        instructions_message = (
            "1. Open the menu \"Config Syntax\" and read it carefully.\n"
            "2. Create a new JSON file with the same syntax as specified.\n"
            "3. Upload the new JSON file.\n"
        )

        instructions_text = tk.Label(
            about_window,
            text=instructions_message,
            font=("Courier", 11),  # Monospace for clear steps
            fg=self.text,
            bg=self.boxes,
            justify=tk.LEFT,
            anchor="nw",
            wraplength=500
        )
        instructions_text.pack(pady=(5, 15), padx=10, fill=tk.BOTH)

        # Revert Section
        revert_message = (
            "Did something wrong? No worries! You can always revert to the default configuration."
        )

        revert_label = tk.Label(
            about_window,
            text=revert_message,
            font=("Arial", 12, "italic"),
            fg="#9E9E9E",  # Grey for subtlety
            bg=self.background,
            wraplength=500,
            justify=tk.LEFT,
            anchor="nw"
        )
        revert_label.pack(pady=(5, 20), fill=tk.BOTH)

        # Close Button
        close_button = tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            bg="#B71C1C",  # Red for attention
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        close_button.pack(pady=10)


    #
    # CUSTOM SOURCE / DESTINATION
    #

    def add_custom_source(self):
        """
        Allows the user to add a custom source directory to the list of allowed sources.
        """
        # Prompt the user to select a folder
        new_source_path = filedialog.askdirectory(title="Select a New Source Folder")
        if new_source_path:
            source_name = os.path.basename(new_source_path)  # Use the folder name as the key
            if new_source_path in self.allowed_sources.values():
                messagebox.showinfo("Source Path Exists", "This source path is already listed.")
            else:
                self.allowed_sources[source_name] = new_source_path
                self.log_progress(f"Source '{source_name}' has been added successfully!")
                messagebox.showinfo("Source Added", f"Source '{source_name}' has been added successfully!")

                # Update the source dropdown after adding the new source
                self.update_source_dropdown()

    def change_destination(self):
        """
        Allows the user to specify a custom destination folder for organizing files.
        Adds '/DeskSave' at the end of the selected destination folder.
        """
        # Prompt the user to select a folder
        new_destination_path = filedialog.askdirectory(title="Select a Destination Folder")
        if new_destination_path:
            # Append /DeskSave to the selected folder path
            new_destination_path = os.path.join(new_destination_path, "DeskSave", self.current_month_year)
            
            # Set the custom destination path
            self.custom_destination_path = new_destination_path
            
            # Ensure the destination directory exists
            os.makedirs(self.custom_destination_path, exist_ok=True)

            self.log_progress(f"Destination path has been set to: {new_destination_path}")
            messagebox.showinfo("Destination Changed", f"Destination path has been set to:\n{new_destination_path}")
        else:
            messagebox.showinfo("Destination Not Changed", "No destination path was selected.")

    def about_paths(self):
        """
        Displays information about configuring custom paths and lists the default paths
        with an enhanced UI for better readability and style.
        """
        # Create a new Toplevel window
        about_window = tk.Toplevel(self)
        about_window.title("About Path Configuration")
        about_window.geometry("550x600")
        about_window.configure(bg=self.background, padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            about_window,
            text="Path Configuration Guide",
            font=("Helvetica", 18, "bold"),
            fg="#4CAF50",  # Green for title
            bg=self.background
        )
        title_label.pack(pady=(10, 20))

        # Explanation Section
        explanation = (
            "You can specify custom source and destination paths to organize your files. "
            "Below are the default paths configured in the application."
        )

        explanation_label = tk.Label(
            about_window,
            text=explanation,
            font=("Arial", 12),
            fg=self.text,
            bg=self.background,
            wraplength=500,
            justify=tk.LEFT,
            anchor="nw"
        )
        explanation_label.pack(pady=(5, 15), fill=tk.BOTH)

        # Default Paths Section
        default_paths_label = tk.Label(
            about_window,
            text="Default Paths:",
            font=("Arial", 14, "bold"),
            fg="#F57C00",  # Orange to emphasize
            bg=self.background,
            anchor="w"
        )
        default_paths_label.pack(fill=tk.X, pady=(10, 5))

        # Path Details
        paths_message = (
            f"1. **Source Paths** (where your files are located):\n"
            f"   - Desktop: {self.allowed_sources['Desktop']}\n"
            f"   - Downloads: {self.allowed_sources['Downloads']}\n\n"
            f"2. **Destination Path** (where the sorted files will be moved to):\n"
            f"   - Documents folder"
        )

        paths_label = tk.Label(
            about_window,
            text=paths_message,
            font=("Courier", 11),  # Monospace for paths
            fg=self.text,
            bg=self.boxes,
            justify=tk.LEFT,
            anchor="nw",
            wraplength=500
        )
        paths_label.pack(pady=(5, 20), padx=10, fill=tk.BOTH)

        # Add a tip
        tip_label = tk.Label(
            about_window,
            text="Tip: Ensure your custom paths are valid to prevent errors during file organization.",
            font=("Arial", 10, "italic"),
            fg="#9E9E9E",  # Grey for subtlety
            bg=self.background,
            wraplength=500,
            justify=tk.LEFT,
            anchor="w"
        )
        tip_label.pack(pady=(5, 20))

        # Close Button
        close_button = tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            bg="#B71C1C",  # Red for emphasis
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        close_button.pack(pady=10)

    #
    # Ignoring data
    # 

    def ignore_data(self):
        """
        Opens a dialog to manage the ignore files and folders.
        It allows the user to add new files/folders to ignore and revert to the default ignore settings.
        """
        # Functionality
        def save_ignore_data():
            """Saves the ignore data (files and folders) to the ignore JSON file."""
            # Get the new ignore files and folders from the input fields
            new_ignore_files = ignore_files_entry.get().split(',') if ignore_files_entry.get() else []
            new_ignore_folders = ignore_folders_entry.get().split(',') if ignore_folders_entry.get() else []

            # Clean up any extra spaces
            self.ignore_files = [item.strip() for item in new_ignore_files]
            self.ignore_folders = [item.strip() for item in new_ignore_folders]

            # Get the path for the ignore.json file (in the same directory as the executable)
            ignore_json_path = self.get_ignore_json_path()
            
            try:
                # Write the updated ignore data to the ignore.json file
                with open(ignore_json_path, 'w', encoding='UTF-8') as json_file:
                    json.dump(
                        {"ignore_files": self.ignore_files, "ignore_folders": self.ignore_folders},
                        json_file,
                        indent=4
                    )
                messagebox.showinfo("Data Saved", "Ignore data updated successfully!")
            except Exception as e: # pylint: disable=broad-exception-caught
                messagebox.showerror("Error", f"An error occurred: {e}")

            ignore_window.destroy()

        def revert_ignore_to_default():
            """
            Reverts the ignore settings to their default values and updates the JSON file.
            """
            # Default ignore files and folders
            default_ignore_files = [".DS_Store"]
            default_ignore_folders = ["DeskSaveApp", "DeskSave"]
            
            # Confirm the revert action with the user
            confirmation = messagebox.askyesno(
                "Revert to Default",
                "Are you sure you want to revert the ignore settings to the default values?"
            )

            if confirmation:
                try:
                    # Update the ignore files and folders in the app
                    self.ignore_files = default_ignore_files
                    self.ignore_folders = default_ignore_folders
                    
                    # Get the path for the ignore.json file (in the same directory as the executable)
                    ignore_json_path = self.get_ignore_json_path()
                    
                    # Write the default settings back to the ignore.json file
                    with open(ignore_json_path, 'w', encoding='UTF-8') as json_file:
                        json.dump(
                            {"ignore_files": default_ignore_files, "ignore_folders": default_ignore_folders},
                            json_file,
                            indent=4
                        )
                    
                    # Update the entry fields to reflect the new default values
                    ignore_files_entry.delete(0, tk.END)  # Clear the existing content
                    ignore_files_entry.insert(tk.END, ', '.join(self.ignore_files))  # Insert default ignore files
                    
                    ignore_folders_entry.delete(0, tk.END)  # Clear the existing content
                    ignore_folders_entry.insert(tk.END, ', '.join(self.ignore_folders))  # Insert default ignore folders

                    messagebox.showinfo("Reverted to Default", "The ignore settings have been reset to the default values.")
                except Exception as e: # pylint: disable=broad-exception-caught
                    messagebox.showerror("Error", f"An error occurred while reverting to the default settings: {e}")
        
        # UI
        # Create a new window for managing ignore data
        ignore_window = tk.Toplevel(self)
        ignore_window.title("Manage Ignore Files and Folders")
        ignore_window.geometry("450x350")
        ignore_window.configure(bg=self.background)

        # Header Label
        header_label = tk.Label(
            ignore_window,
            text="Manage Ignore Files and Folders",
            font=("Helvetica", 16, "bold"),
            fg=self.text,
            bg=self.background
        )
        header_label.pack(pady=(20, 10))

        # Instructions Label
        instructions_label = tk.Label(
            ignore_window,
            text="Specify files and folders to ignore during organization.",
            font=("Arial", 12),
            fg=self.text,
            bg=self.background
        )
        instructions_label.pack(pady=(5, 15))

        # Ignore Files Label and Entry
        ignore_files_label = tk.Label(
            ignore_window,
            text="Ignore Files (comma-separated):",
            font=("Arial", 12, "bold"),
            fg=self.text,
            bg=self.background,
            anchor="w"
        )
        ignore_files_label.pack(fill=tk.X, padx=20, pady=5)

        ignore_files_entry = tk.Entry(
            ignore_window,
            width=50,
            font=("Arial", 12),
            bg=self.boxes,
            fg=self.text,
            relief=tk.GROOVE
        )
        ignore_files_entry.insert(tk.END, ', '.join(self.ignore_files))
        ignore_files_entry.pack(fill=tk.X, padx=20, pady=5)

        # Ignore Folders Label and Entry
        ignore_folders_label = tk.Label(
            ignore_window,
            text="Ignore Folders (comma-separated):",
            font=("Arial", 12, "bold"),
            fg=self.text,
            bg=self.background,
            anchor="w"
        )
        ignore_folders_label.pack(fill=tk.X, padx=20, pady=5)

        ignore_folders_entry = tk.Entry(
            ignore_window,
            width=50,
            font=("Arial", 12),
            bg=self.boxes,
            fg=self.text,
            relief=tk.GROOVE
        )
        ignore_folders_entry.insert(tk.END, ', '.join(self.ignore_folders))
        ignore_folders_entry.pack(fill=tk.X, padx=20, pady=5)

        # Button Frame for alignment
        button_frame = tk.Frame(ignore_window, bg=self.background)
        button_frame.pack(pady=20)

        # Save Button
        save_button = tk.Button(
            button_frame,
            text="Save Changes",
            command=save_ignore_data,
            bg="#4CAF50",  # Green
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        save_button.grid(row=0, column=0, padx=10)

        # Revert to Default Button
        revert_button = tk.Button(
            button_frame,
            text="Revert to Default",
            command=revert_ignore_to_default,
            bg="#F57C00",  # Orange
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        revert_button.grid(row=0, column=1, padx=10)

        # Close Button
        close_button = tk.Button(
            button_frame,
            text="Close",
            command=ignore_window.destroy,
            bg="#B71C1C",  # Red
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        close_button.grid(row=0, column=2, padx=10)

        # Footer Label
        footer_label = tk.Label(
            ignore_window,
            text="Tip: Use commas to separate entries (e.g., file1.txt, file2.txt).",
            font=("Arial", 10, "italic"),
            fg="#9E9E9E",
            bg=self.background
        )
        footer_label.pack(pady=(5, 10))

    def about_ignoring(self):
        """
        Opens a custom window with information on how to ignore files and folders.
        Provides a detailed explanation with a visually appealing layout.
        """
        # Create a new Toplevel window
        about_window = tk.Toplevel(self)
        about_window.title("About Ignoring Files and Folders")
        about_window.geometry("550x600")
        about_window.configure(bg=self.background, padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            about_window,
            text="Ignoring Files and Folders",
            font=("Helvetica", 18, "bold"),
            fg="#4CAF50",  # Green text
            bg=self.background
        )
        title_label.pack(pady=(10, 20))

        # Explanation Text
        explanation = (
            "You can specify files and folders that the file organizer should ignore.\n\n"
            "This allows you to prevent certain items from being moved or modified during file organization.\n\n"
            "Your configuration is saved locally on your machine, ensuring privacy and ease of use. "
            "You can also revert to the default ignore settings at any time."
        )

        explanation_label = tk.Label(
            about_window,
            text=explanation,
            font=("Arial", 12),
            fg=self.text,
            bg=self.background,
            wraplength=460,  # Limit the text width
            justify=tk.LEFT,
            anchor="nw"
        )
        explanation_label.pack(pady=10, fill=tk.BOTH, expand=True)

        # Add an icon or tip (optional)
        tip_label = tk.Label(
            about_window,
            text="Tip: Use the ignore settings to exclude system files or frequently used directories!",
            font=("Arial", 10, "italic"),
            fg="#F57C00",  # Orange text
            bg=self.background,
            anchor="w",
            wraplength=460,
            justify=tk.LEFT
        )
        tip_label.pack(pady=(5, 20))

        # Close Button
        close_button = tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            bg="#B71C1C",  # Red
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        close_button.pack(pady=10)
    
    #
    # About
    #

    def show_about(self):
        """
        Displays information about the DeskSave application, including the version,
        in a visually engaging way using a custom Toplevel window.
        """
        app_version = os.getenv("APP_VERSION", "NO_OFFICIAL_RELEASE")  # Default version if not from official build

        # About message
        about_message = (
            f"DeskSave Application\n\n"
            f"Version {app_version}\n"
            "A simple file organization tool for sorting files into predefined categories based on their extensions.\n"
            "Developed by Lars Kühn."
        )

        # Create a Toplevel window for the "About" dialog
        about_window = tk.Toplevel(self)
        about_window.title("About DeskSave")
        about_window.geometry("550x600")
        about_window.configure(bg=self.background, padx=20, pady=20)

        # Title Label
        title_label = tk.Label(
            about_window,
            text="DeskSave Application",
            font=("Helvetica", 18, "bold"),
            fg="#4CAF50",  # Green for a fresh and professional feel
            bg=self.background
        )
        title_label.pack(pady=(20, 10))

        # Version Label
        version_label = tk.Label(
            about_window,
            text=f"Version {app_version}",
            font=("Arial", 14, "italic"),
            fg="#FF9800",  # Orange to highlight the version number
            bg=self.background
        )
        version_label.pack(pady=5)

        # Description Label
        description_label = tk.Label(
            about_window,
            text="A simple file organization tool for sorting files based on extensions.",
            font=("Arial", 12),
            fg=self.text,
            bg=self.background,
            wraplength=450,
            justify=tk.CENTER
        )
        description_label.pack(pady=(10, 20))

        # Developer Info
        developer_label = tk.Label(
            about_window,
            text="Developed by Lars Kühn",
            font=("Arial", 12, "bold"),
            fg="#9E9E9E",  # Grey for subtle and professional touch
            bg=self.background
        )
        developer_label.pack(pady=10)

        # About Message Text Area (remove redundant label)
        about_text_area = tk.Label(
            about_window,
            text=about_message,
            font=("Courier", 11),
            fg=self.text,
            bg=self.background,
            justify=tk.LEFT,
            anchor="nw",
            wraplength=450
        )
        about_text_area.pack(pady=(10, 20))  # This replaces the label that previously doubled the text

        # Close Button
        close_button = tk.Button(
            about_window,
            text="Close",
            command=about_window.destroy,
            bg="#B71C1C",  # Red to stand out
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        )
        close_button.pack(pady=10)


    #
    # UI Helper Functions
    #

    def log_progress(self, message):
        """
        Logs progress in the progress text box.
        """
        self.progress_text_box.config(state=tk.NORMAL)
        self.progress_text_box.insert(tk.END, f"{message}\n")
        self.progress_text_box.config(state=tk.DISABLED)

    def update_source_dropdown(self):
        """
        Updates the source dropdown menu after a new source is added.
        """
        self.source_combobox['values'] = list(self.allowed_sources.values())
        self.source_combobox.set(list(self.allowed_sources.values())[-1])

    #
    # Create widgets
    #

    def create_widgets(self):
        """
        Creates the main widgets for the GUI with enhanced visual design.
        """
        # Header Label
        header_label = tk.Label(
            self,
            text="DeskSave File Organizer",
            font=("Helvetica", 20, "bold"),
            fg=self.text,
            bg=self.background
        )
        header_label.pack(pady=(20, 10))

        # Source Dropdown Label
        self.source_label = tk.Label(
            self,
            text="Select Source Folder:",
            font=("Arial", 16, "bold"),
            fg=self.text,
            bg=self.background,
            anchor="w"
        )
        self.source_label.pack(fill=tk.X, padx=20, pady=(10, 5))

        # Source Dropdown Combobox
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=self.boxes,
            background=self.boxes,
            foreground=self.text,
            font=("Arial", 14)
        )
        self.source_combobox = ttk.Combobox(
            self,
            values=list(self.allowed_sources.values()),
            state="readonly",
            style="TCombobox"
        )
        self.source_combobox.pack(fill=tk.X, padx=20, pady=5)

        # Start Button
        self.start_button = tk.Button(
            self,
            text="Start Organizing",
            command=self.organize_files,
            bg=self.menu,
            activebackground="#3D6F6F",  # Slightly darker for hover effect
            fg=self.text,
            font=("Arial", 16, "bold"),
            relief=tk.RAISED,
            bd=3
        )
        self.start_button.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Progress Text Box Label
        progress_label = tk.Label(
            self,
            text="Progress Log:",
            font=("Arial", 14, "bold"),
            fg=self.text,
            bg=self.background,
            anchor="w"
        )
        progress_label.pack(fill=tk.X, padx=20, pady=(10, 5))

        # Progress Text Box
        self.progress_text_box = tk.Text(
            self,
            height=12,
            state=tk.DISABLED,
            bg=self.boxes,
            fg=self.text,
            font=("Courier", 12),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2
        )
        self.progress_text_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

        # Footer Label
        footer_label = tk.Label(
            self,
            text="Tip: Select the folder and click 'Start Organizing' to begin!",
            font=("Arial", 10, "italic"),
            fg="#9E9E9E",
            bg=self.background
        )
        footer_label.pack(pady=(5, 10))

    #
    # Logical functions
    # 
    
    def load_file_types(self):
        """
        Loads the file types from the default JSON configuration file.
        """
        try:
            with open(self.default_json_path, 'r', encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Configuration file not found.")
            sys.exit()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Configuration file is invalid.")
            sys.exit()

    def get_ignore_json_path(self):
        """Returns the correct path for ignore.json based on the executable's directory."""
        # Get the directory where the executable is located
        executable_dir = os.path.dirname(sys.executable)  # This is the directory of the executable
        ignore_json_path = os.path.join(executable_dir, 'ignore.json')
        return ignore_json_path

    def load_ignore_json(self):
        """Loads the ignore JSON file and returns ignore files and folders."""
        ignore_json_path = self.get_ignore_json_path()

        # Default ignore data (hardcoded in the script)
        default_ignore_files = [".DS_Store"]
        default_ignore_folders = ["DeskSaveApp", "DeskSave"]
        
        try:
            # Try to load the ignore data from the user's file system
            with open(ignore_json_path, 'r', encoding='UTF-8') as f:
                ignore_data = json.load(f)
                ignore_files = ignore_data.get('ignore_files', default_ignore_files)
                ignore_folders = ignore_data.get('ignore_folders', default_ignore_folders)
                return ignore_files, ignore_folders
        except FileNotFoundError:
            # If the file doesn't exist, return default ignore data
            print(f"Warning: {ignore_json_path} not found. Using default ignore lists.")
            return default_ignore_files, default_ignore_folders
        except json.JSONDecodeError:
            # If there's a problem decoding the JSON, use default ignore data
            print(f"Error: Failed to decode JSON from {ignore_json_path}. Using default ignore lists.")
            return default_ignore_files, default_ignore_folders

    def organize_files(self):
        """
        Organizes files from the selected source folder into the specified categories based on their extensions.
        """

        # Set destination‚
        destination = self.custom_destination_path or self.default_destination_path

        # Ensure destination exists
        os.makedirs(destination, exist_ok=True)

        # Get the selected source folder from the dropdown
        selected_source = self.source_combobox.get()


        if selected_source:
            self.log_progress(f"Organizing files from: {selected_source}")
        
            self.move_files(selected_source, destination, self.file_types, self.ignore_files, self.ignore_folders)
            self.log_progress("Files have been organized successfully!")
        else:
            messagebox.showerror("Error", "Invalid source folder.")

    def move_files(self, source, destination, file_types, ignore_files, ignore_folders):
        """
        Moves and organizes files from the source directory to the destination directory,
        categorizing them based on their file types and the configuration specified in
        'file_types.json'.

        Files and folders can be excluded from the organization process based on the
        `ignore_files` and `ignore_folders` lists. After moving files, it attempts to delete
        any empty folders left in the source directory.
        """
        
        for item in os.listdir(source):
            full_path = os.path.join(source, item)
            
            # ignore folders that are in the ignore list
            if os.path.isdir(full_path) and item in ignore_folders:
                self.log_progress(f"Ignoring folder: {item}")
                continue
            
            # ignore files that are in the ignore list or hidden files (e.g., .DS_Store)
            if item in ignore_files or item.startswith('.'):
                self.log_progress(f"Ignoring file: {item}")
                continue
            
            # Process directories: move their contents to the appropriate file type folder
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
            
            # Process files: move them to the appropriate file type folder
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

if __name__ == "__main__":
    app = DeskSaveApp()
    app.mainloop()
