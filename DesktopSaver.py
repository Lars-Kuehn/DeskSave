import os; import getpass; import datetime # Import modules
if __name__ == '__main__':
    date = datetime.datetime.today() # Get current date
    date = str(date.strftime("%m-%Y")) # Only display month and year 
    source = '/Users/'+getpass.getuser()+'/Desktop/' # Source, from where the files are moved
    destination = '/Users/'+getpass.getuser()+'/Documents/Desktop-'+date+'/' # Destination, where the files are moved
    directories = os.listdir(source) # Get the whole directory of the source
    for file in directories:
        try:
            if file == 'DesktopSaver.py' or file == '.DS_Store' or file == '.localized': # If-Statement so important files do not get moved
                continue
            os.renames(source+file, destination+file) # Function that moves the files
        except: # If any error is caught, skip the file.
            continue
            
