from subprocess import check_output

def getname():
    raw = check_output(["wmic", "path", "win32_VideoController", "get", "name"])
    rawdecoded = raw.decode()
    getname = rawdecoded.strip("Name").rstrip("\n").replace("\n", "")
    return getname
