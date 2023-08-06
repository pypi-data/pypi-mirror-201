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

B R E A D
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

import cpu
import disk
import gpu
import memory
import software

