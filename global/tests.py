from django.test import TestCase

# Create your tests here.
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