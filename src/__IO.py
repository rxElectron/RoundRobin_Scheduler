#!/bin/python3

######################################
#                                    #
#  @  filename    : __IO.py          #
#    Developer   : Reza Khodarahimi #
#  﫥  Copyright     2024             #
#                                    #
######################################

# __IO.py
from __OS import *
from __SRCs import *
from __PROCESS import *

def read_processes(filename,gui):
    processes = []
    process = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Cpu:"):
                if process:
                    processes.append(process)
                process = PROCESS(gui)
                process.CPU = list(map(int, re.findall(r'\d+', line)))
            elif line.startswith("IO:"):
                if process:
                    process.IO = list(map(int, re.findall(r'\d+', line)))
        if process:
            processes.append(process)

    return processes

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see("end")

    def flush(self):
        pass
    
def print_message(text_widget, message, tag="default"):
    text_widget.configure(state="normal")
    text_widget.insert("end", message + "\n", tag)
    text_widget.configure(state="disabled")
    text_widget.see("end")