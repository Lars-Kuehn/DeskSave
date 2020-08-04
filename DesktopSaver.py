import os; import getpass; import datetime
if __name__ == '__main__':
    date = datetime.datetime.today()
    date = str(date.strftime("%m-%Y"))
    source = '/Users/'+getpass.getuser()+'/Desktop/'
    destination = '/Users/'+getpass.getuser()+'/Documents/Desktop-'+date+'/'
    directories = os.listdir(source)
    for file in directories:
        try:
            if file == 'DesktopCleaner.py' or file == '.DS_Store' or file == '.localized': 
                continue
            os.renames(source+file, destination+file)
        except:
            continue
            
