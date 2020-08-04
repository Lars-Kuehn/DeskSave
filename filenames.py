order = ['compressed', 'audio', 'disc', 'data', 'email', 'executable', 
            'font', 'pictures', 'presentation', 'spreadsheet', 'text', 'video']


def compressed():
    compressedExtension = ['rar', 'zip', '7z', 'arj', 'deb', 'pkg', 'rpm', 'z']
    return(compressedExtension, len(compressedExtension))

def audio():
    audioExtension = ['aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'wpl']
    return(audioExtension, len(audioExtension))

def disc():
    discExtension = ['bin', 'dmg', 'iso', 'toast', 'vcd']
    return(discExtension, len(discExtension))

def data():
    dataExtension = ['csv', 'dat', 'db', 'dbf', 'log', 'mdb', 'sav', 'sql', 'tar', 'xml']
    return(dataExtension, len(dataExtension))

def email():
    emailExtension = ['email', 'eml', 'emlx', 'msg', 'oft', 'ost', 'pst', 'vcf']
    return(emailExtension, len(emailExtension))

def executable():
    executableExtension = ['apk', 'bat', 'bin', 'cgi', 'pl', 'com', 'exe', 'gadget', 'jar', 'msi', 'py', 'wsf']
    return(executableExtension, len(executableExtension))

def font():
    fontExtension = ['fnt', 'fon', 'otf', 'ttf']
    return(fontExtension, len(fontExtension))

def pictures(): 
    pictureExtension = ['jpg', 'png', 'gif', 'webp', 'tiff', 'psd', 'raw', 'bmp', 'heif', 'indd', 'jpeg', 'psd', 'svg', 'ps', 'ai']
    return (pictureExtension, len(pictureExtension))

def presentation():
    presentationExtension = ['key', 'odp', 'pps', 'ppt', 'pptx']
    return(presentationExtension, len(presentationExtension))

def spreadsheet():
    spreadsheetExtension = ['ods', 'xls', 'xlsm', 'xlsx']
    return(spreadsheetExtension, len(spreadsheetExtension))

def text():
    textExtension = ['doc', 'docx', 'odt', 'pdf', 'rtf', 'tex', 'txt', 'wpd']
    return(textExtension, len(textExtension))

def video():
    videoExtension = ['avi', 'flv', 'h264', 'm4v', 'mkv', 'mov', 'mp4', 'mpg', 'wmv']
    return(videoExtension, len(videoExtension))
