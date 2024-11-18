# DeskSave

DeskSave is a simple yet powerful tool designed to automate the organization of files by moving them from your source directory to your destination directory. It categorizes files based on their data type and file extensions, simplifying file management and reducing clutter.

## Features

- **Graphical User Interface (GUI)**: DeskSave provides a clean, user-friendly GUI to easily interact with the application.
- **Customizable JSON Configuration File**: The application uses a `file_types.json` configuration file (located in `\script\file_types.json`) to recognize and categorize various file types. You can easily upload your own configuration file via the GUI.
- **CI/CD Pipeline**: This repository includes a CI/CD pipeline to ensure the quality of the code through *Pylint*, maintaining clean, efficient code throughout development.

## Folder Structure: `\script`

This directory contains the core Python script and necessary configuration files.

### Files
- **`main.py`**: The Python script that handles the file-moving logic, including sorting files based on their extensions.
- **`file_types.json`**: A JSON file that maps file extensions to categories. You can modify or extend this file by adding new file types, or upload a custom configuration via the GUI.

## Roadmap for DeskSave

### Currently in Development
- **Save File Type Configurations**: Users will soon be able to save their custom file type configurations. Unlike the "ignore" settings, file type configurations are not yet saved between sessions. Future versions will allow users to store multiple configurations and select them upon restarting the application.

### Planned Updates
- **Automated Sorting**: Plans to add an automatic sorting feature that will allow files to be organized periodically on a set schedule, without manual intervention.

## Disclaimer

### **Executables**
DeskSave includes two executables with each release: one for **Windows** and one for **macOS**. Since this project is not professionally notarized, your operating system may display warnings when attempting to run these executables. If this occurs, you can always download the source code and run the `main.py` script directly from the `script` directory.

### **Use at Your Own Risk**
While DeskSave is intended to simplify file organization, users should exercise caution. There is always the potential for accidental file movement or deletion, particularly if the configuration file is not correctly set up. **Always back up important files before using DeskSave**, and double-check your configuration settings. The author assumes no responsibility for any data loss or other issues caused by using this tool.

## Author
Lars Kühn  
[GitHub Profile](https://github.com/Lars-Kuehn)

---

### Recent Changes:
- **Enhanced GUI**: Users can now select both source and destination folders within the GUI.
- **Progress Log**: A new progress log tracks and displays which files have been moved during the sorting process.
- **Custom Configuration Upload**: Users can upload their own configuration file to define which file types should be moved and how they should be categorized.
- **File & Folder Ignore Settings**: Users can specify files and folders to ignore in the application settings, ensuring certain files are excluded from the sorting process.
