import os; import getpass; import datetime; import fileData # Import modules

def main():
    date = datetime.datetime.today() # Get current date
    date = str(date.strftime("%m-%Y")) # Only display month and year 
    source = '/Users/'+getpass.getuser()+'/Desktop/' # Source, from where the files are moved
    destination = '/Users/'+getpass.getuser()+'/Documents/Desktop-'+date+'/' # Destination, where the files are moved
    directories = os.listdir(source) # Get the whole directory of the source
    for file in directories:
        try:
            if file == 'DesktopSort.py' or file == 'fileData.py' or file == '.DS_Store' or file == '.localized': # If-Statement so important files do not get moved
                continue
            for w in range(0,12): # Go through the different functions in fileData.py
                temp = getattr(fileData, fileData.order[w])()
                content, length = temp # Get the length of how many datatypes one function
                for x in range(0, length): # Go through each of the datatypes
                    if str(file).split('.')[-1] == getattr(fileData, fileData.order[w])()[0][x]: # Find a match
                        os.renames(source+file, destination+fileData.order[w]+'/'+file) # Move file
                
        except: # When error is caught, continue

if __name__ == '__main__':
    main()