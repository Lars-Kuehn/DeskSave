import os; import getpass; import datetime; import fileData # Import modules
if __name__ == '__main__':
    date = datetime.datetime.today() # Get current date
    date = str(date.strftime("%Y-%m")) # Only display month and year
    source = '/Users/'+getpass.getuser()+'/Desktop/' # Source, from where the src are moved
    destination = '/Users/'+getpass.getuser()+'/Documents/Desktops/'+date+'/' # Destination, where the src are moved
    directories = os.listdir(source) # Get the whole directory of the source
    for file in directories:
        try:
            if file == 'DesktopSaver.py' or file == '.DS_Store' or file == '.localized': # If-Statement so important src do not get moved
                continue
            for w in range(0,12): #
                temp = getattr(fileData, fileData.order[w])();
                content, length = temp
                for x in range(0, length):
                    if str(file).split('.')[-1] == getattr(fileData, fileData.order[w])()[0][x]:
                        os.renames(source + file, destination + fileData.order[w] + '/' + file) # Moves file
                
        except:
            continue