import os; import getpass; import datetime; import filenames # Import modules
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
            for w in range(0,12):
                temp = getattr(filenames, filenames.order[w])()
                content, length = temp
                for x in range(0, length):
                    if str(file).split('.')[-1] == getattr(filenames, filenames.order[w])()[0][x]:
                        os.renames(source+file, destination+filenames.order[w]+'/'+file)
                
        except Exception as e:
            print(str(e))