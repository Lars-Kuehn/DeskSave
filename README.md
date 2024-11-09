# DeskSave
This application is able to move your files from your desktop or download folder to your Documents and structures them according to the data-type. 

## What is the DeskSave capable of?
- **Graphical User Interface**: The application is run trough an GUI.
- **JSON configuration file**: `\script\file_types.json` contains all of the file-types that are being recognised by the application.
- **CI/CD**: This repository contains an CI/CD pipeline that checks if all of its python code is being correct via *Pylint*.

## `\script`
The python script and the JSON file lie in this directory.
### Files
- `deskSave.py`: Python Script with file-moving logic.
- `file_types.json`: JSON File with all file types. You can add additional file types.

## Roadmap for DeskSave
### Currently in development
- **Executable File**: Launch DeskSave via one executable file.

### Planned updates
- **Select directory**: The user should be able to Source- and Destination Folder.
- **Settings**: The user should be able to change the Settings of the application in the GUI.

## Disclaimer
**Use at Your Own Risk**  
DeskSave is intended to help organize files, but it may delete or move files incorrectly. Users are advised to thoroughly review the configuration and backup important files before using DeskSave. The author assumes no responsibility for any loss or damage to data.

## Author
Lars Kühn [https://github.com/Lars-Kuehn]