# Winfo
Winfo is a Python Library for getting System Stats (Made for Windows)

## Features
List of all features:
### Processor Information

- Get Brandname (Name you see in Taskmanager)
- Get "real" name
- Get Maximum Clock Speed
- Get amount of cores
- Get amount of threads
- Get Architecture

```Python
import Winfo

print("I have an " + Winfo.cpu.getbrandname())
print("It's real name is " + Winfo.cpu.getrealname())
print("This monster works at " + Winfo.cpu.MaxClockSpeed() + " Ghz")
print("It has" + str(Winfo.cpu.cores()) + " Cores and " + str(Winfo.cpu.threads) + " Threads")
print("CPU Architecture: " + Winfo.cpu.architecture())
```

### GPU Information

- Get Brandname of GPU
- Get Refresh Rate

```Python
import Winfo

print("My GPU is the " + Winfo.gpu.getname())
print("I like my " + Winfo.gpu.getRefreshRate() + " Hz")
```

### Memory Information

- Get Memory manufacturer
- Get total Memory capacity (MB)
- Get total Memory capacity (GB)
- Get Memory Speed

```Python
import Winfo

print("My Memory is from " + Winfo.memory.getmanufacturer())
print("I've " + Winfo.memory.getcapacityMB() + " of memory or in GB: " + Winfo.memory.getcapacityGB())
print("My memory works at " + Winfo.memory.getSpeed() + " Mhz")
```

### Disk Information

- List all connected disks (Returns them in a Python list)
- Get Disk Size (Capacity) of disk 0, if you want to get the size of another disks set it's number as the index argument in the function

```Python
import Winfo

print("Here's a list of all my disks as a Python List: " + str(Winfo.disk.listall()))
print("The size of my primary disk is: " + Winfo.disk.getsize())
print("The size of my secondary disk is: " + Winfo.disk.getsize(1))
```

- BONUS TIP! If you want to list all disks in a prettier way try this:

```Python
import Winfo

prettylist = ""

for i in Winfo.disk.listall():
    prettylist = prettylist + i + "\n"

print(prettylist)
```

- Instead of looking like this when printed:

```
['Disk 0', 'Disk 1', 'Disk 2']
```

- It would now look like this:

```
Disk 0
Disk 1
Disk 2

```
### Ethernet Information (Adapters)

- Get MAC Address (Please read disclaimer, which can be found in the source code of this project)
- List all recognized Network Adapters

```Python
import Winfo

print("My MAC Address is: " + Winfo.ethernet.macaddr())
print("List of all Network Adapters as a Python list: " + Winfo.ethernet.listadapters())
```

- Like with the Disklist, you can make the list returned from Winfo.ethernet.listadapters() way prettier by doing this:

```Python
import Winfo

prettylist = ""

for i in Winfo.ethernet.listadapters():
    prettylist = prettylist + i + "\n"

print(prettylist)
```
- Instead of looking like this when printed:

```
['Adapter 1', 'Adapter 2', 'Adapter 3']
```

- It would now look like this:

```
Adapter 1
Adapter 2
Adapter 3

```

### Motherboard Information

- Get Brandname of your Motherboard
- Get Manufacturer of your Motherboard

```Python
import Winfo

print("My Motherboard is an " + Winfo.motherboard.getname() + " , made by " + Winfo.motherboard.getmanufacturer())
```

### Software Information

- Get current Windows version
- Get current Windows release
- Get device name
- Get user name

```Python
import Winfo

print("I'm current running Windows " + Winfo.software.system() + " on version " + Winfo.software.version())
print("I named my computer " + Winfo.software.devicename())
print("I'm logged in as " + Winfo.software.username())
```
## Questions you might have:

- Q: How can I install this library? A: pip install Winfo
- Q: MacOS/Linux/BSD Support? A: Windows-only.
- Q: What can I do with the code? A: Read the license (CC BY-SA 4.0)

### If you've further questions, join our [discord](https://discord.gg/jDAGR26yXe)!

## License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/BLUEAMETHYST-Studios/Winfo">Winfo</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://blueamethyst.me">BLUEAMETHYST Studios</a> is licensed under <a href="http://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>
