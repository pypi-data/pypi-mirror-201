from subprocess import check_output

def listall():
    raw = check_output(["wmic", "diskdrive", "get", "Caption"], shell=True)
    rawdecoded = raw.decode()
    disks = [line.replace("Caption", "").strip() for line in rawdecoded.split("\n")[1:] if line.strip() != ""]
    return disks

def getsize(index = 0):
    raw = check_output(["wmic", "diskdrive", "get", "Size"], shell=True)
    rawdecoded = raw.decode()
    size = rawdecoded.replace("Size", "")
    sizeaslist = size.split("\n")
    c = 0
    for i in sizeaslist:
        if index + 1 == c:
            size = i
            break
        else:
            c = c + 1
    if size == "\r\r":
        raise IndexError("Disk Index invalid.")
    elif index < 0:
        raise IndexError("Disk Index invalid.")
    elif size == "":
        raise IndexError("Disk Index invalid.")
    elif size == "           \r\r":
        raise IndexError("Disk Index invalid.")
    return int(size)


print(listall())

