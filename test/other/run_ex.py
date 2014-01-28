import serial



# ser = serial.Serial('/dev/tty0',9600)
# while True:
#     print ser.readline()

import Tkinter


root = Tkinter.Tk()

tcl_script ="""
    load "/srv/develop/audela/bin/libmc.so"
    set a [mc_ephem sun]
    puts $a 
    } 
"""

# call the Tkinter tcl interpreter
root.tk.call('eval', tcl_script)
root.mainloop()
