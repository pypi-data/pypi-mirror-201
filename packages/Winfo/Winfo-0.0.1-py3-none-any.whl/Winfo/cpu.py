from subprocess import check_output

def getbrandname():
    raw = check_output(["wmic", "cpu", "get", "name"])
    rawdecoded = raw.decode()
    getname = rawdecoded.strip("Name").rstrip("\n").replace("\n", "")
    return getname

def getrealname():
    raw = check_output(["wmic", "cpu", "get", "caption"])
    rawdecoded = raw.decode()
    getcaption = rawdecoded.strip("Caption").rstrip("\n").replace("\n", "")
    return getcaption

def maxclockspeed():
    raw = check_output(["wmic", "cpu", "get", "MaxClockSpeed"])
    rawdecoded = raw.decode()
    getmax = rawdecoded.strip("MaxClockSpeed").rstrip("\n").replace("\n", "")
    return getmax

def cores():
    raw = check_output(["wmic", "cpu", "get", "NumberOfCores"])
    rawdecoded = raw.decode()
    getcores = rawdecoded.strip("NumberOfCores").rstrip("\n").replace("\n", "")
    return int(getcores)

def threads():
    raw = check_output(["wmic", "cpu", "get", "ThreadCount"])
    rawdecoded = raw.decode()
    getthreads = rawdecoded.strip("ThreadCount").rstrip("\n").replace("\n", "")
    return int(getthreads)