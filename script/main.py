import os
import getpass
import datetime
import json
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class DeskSaveApp(tk.Tk):
    def __init__(self):
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
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(script_dir, 'file_types.json')
            with open(json_path, 'r', encoding='UTF-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Failed to load file types configuration.")
            sys.exit()
    
    def create_widgets(self):
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
        self.progress_text.config(state="normal")
        self.progress_text.insert(tk.END, f"{message}\n")
        self.progress_text.config(state="disabled")
        self.progress_text.see(tk.END)
        
    def organize_files(self):
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
