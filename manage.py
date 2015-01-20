#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OcevuFTCC.settings")

    from django.core.management import execute_from_command_line
    
#     execfile('/home/ros/workspace/OcevuFTCC/monitoring/monitoring.py')
    

    print ("Manage py start")
    execute_from_command_line(sys.argv)
    