from subprocess import check_output

def version():
    raw = check_output(["ver"], shell=True)
    rawdecoded = raw.decode()
    winversion = rawdecoded.replace("Microsoft Windows [Version ", "").replace("]", "").replace("\n", "")
    return winversion

def system():
    if version().startswith("10.0.2"):
        return "11" # because Windows 11 version says 10.0.20 or higher (Microsoft was kinda lazy)
    elif version().startswith("10.0"):
        return "10"
    elif version().startswith("8.1"):
        return "8.1"
    elif version().startswith("8"):
        return "8"
    elif version().startswith("7"):
        return "7"
    else:
        return None # None means not found
    
def devicename():
    raw = check_output(["wmic", "cpu", "get", "SystemName"])
    rawdecoded = raw.decode()
    getdevname = rawdecoded.strip("SystemName").rstrip("\n").replace("\n", "")
    return getdevname

def username():
    raw = check_output(["echo", "%USERNAME%"], shell=True)
    rawdecoded = raw.decode()
    getusername = rawdecoded.replace("\n", "")
    return getusername


    
