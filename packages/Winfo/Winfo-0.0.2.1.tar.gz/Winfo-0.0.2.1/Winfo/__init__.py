"""
Winfo - Python Library

Winfo allows you to get information about your Windows System, it was designed for Windows and won't work on other Operating Systems!

You can get information about your:

- Processor
- Disks
- GPU
- Memory
- Software (Operating System)

The source code is available at our Github:
https://BLUEAMETHYST-Studios/Winfo

              ██████████    
            ████▒▒▒▒██████  
        ████▒▒▒▒▒▒▒▒▒▒██████
      ████▒▒████▒▒▒▒▒▒▓▓████
    ████▒▒▒▒▒▒▒▒██▒▒▒▒▓▓████
    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓████
  ██▒▒████▒▒▒▒▒▒▒▒▒▒▓▓████  
████▒▒▒▒▒▒██▒▒▒▒▒▒▓▓▓▓██    
██▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓████      
██▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓██        
██▒▒▒▒▒▒▒▒▓▓▓▓████          
██▒▒▒▒▒▒▒▒▓▓▓▓██            
  ████▓▓▓▓████              
    ████████                

B      R      E      A      D
"""
# ADDITIONAL INFORMATION
# ======================
# |                    |
# ▼                    ▼

License = """
Winfo by BLUEAMETHYST Studios is licensed under CC BY-SA 4.0. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/4.0/


Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
"""

OtherOS = """
Why isn't Winfo crossplatform-compatible?

Winfo isn't crossplatform-compatible, because this just takes time and a lot of effort and
Windows makes it really easy to get System Information.

So, it's currently not worth it and there's a reason it's called "Winfo" at the time.
"""

from subprocess import check_output

class cpu:
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
  
class gpu:
  def getname():
    raw = check_output(["wmic", "path", "win32_VideoController", "get", "name"])
    rawdecoded = raw.decode()
    getname = rawdecoded.strip("Name").rstrip("\n").replace("\n", "")
    return getname
  def getRefreshRate():
    raw = check_output(["wmic", "path", "win32_VideoController", "get", "CurrentRefreshRate"], shell=True)
    rawdecoded = raw.decode()
    getrate = rawdecoded.replace("CurrentRefreshRate", "").replace("\n", "")
    return int(getrate)
  
class memory:
  def getmanufacturer():
    raw = check_output(["wmic", "cpu", "get", "caption"])
    rawdecoded = raw.decode()
    getmanu = rawdecoded.strip("Caption").rstrip("\n").replace("\n", "")
    return getmanu

  def getcapacityMB():
    raw = check_output(["wmic", "computersystem", "get", "totalphysicalmemory"])
    rawdecoded = raw.decode().lstrip("TotalPhysicalMemory").rstrip("\n")
    getcapMB = int(rawdecoded) / 1024 ** 2
    return int(getcapMB)

  def getcapacityGB():
    raw = check_output(["wmic", "computersystem", "get", "totalphysicalmemory"])
    rawdecoded = raw.decode().lstrip("TotalPhysicalMemory").rstrip("\n")
    getcapGB = int(rawdecoded) / 1024 ** 3
    return int(getcapGB)

  def getSpeed():
    raw = check_output(["wmic", "memorychip", "get", "Speed"])
    rawdecoded = raw.decode().lstrip("Speed").rstrip("\n")
    getspeed = rawdecoded.replace("\n", "")
    return int(rawdecoded)
  
class disk:
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

class ethernet:
  def macaddr():
    """
    DISCLAIMER
    
    May not be true!
    
    If it isn't true, please don't contact us, because this function basically gets it from the getmac-Command in Windows.
    So this basically relies on Windows' Shell.
    
    """
    raw = check_output(["getmac"], shell=True)
    mac = raw.decode().strip().split("\n")[2].split()[0]
    return mac
  
  def listadapters():
    raw = check_output(["wmic", "nic", "get", "name"], shell=True)
    rawdecoded = raw.decode()
    maclist = [line.replace("Caption", "").strip() for line in rawdecoded.split("\n")[1:] if line.strip() != ""]
    return maclist
  
class motherboard:
  def getname():
    raw = check_output(["wmic", "baseboard", "get", "product"], shell=True)
    rawdecoded = raw.decode()
    getboard = rawdecoded.replace("Product", "").replace("\n", "")
    return getboard
  def getmanufacturer():
    raw = check_output(["wmic", "baseboard", "get", "manufacturer"], shell=True)
    rawdecoded = raw.decode()
    getmanu = rawdecoded.replace("Manufacturer", "").replace("\n", "")
    return getmanu
    
class software:
  def version():
    raw = check_output(["ver"], shell=True)
    rawdecoded = raw.decode()
    winversion = rawdecoded.replace("Microsoft Windows [Version ", "").replace("]", "").replace("\n", "")
    return winversion

  def system():
    if software.version().startswith("10.0.2"):
        return "11" # because Windows 11 version says 10.0.20 or higher (Microsoft was kinda lazy)
    elif software.version().startswith("10.0"):
        return "10"
    elif software.version().startswith("8.1"):
        return "8.1"
    elif software.version().startswith("8"):
        return "8"
    elif software.version().startswith("7"):
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
