#!/bin/python3

######################################
#                                    #
#  @  filename    : __SRCs.py        #
#    Developer   : Reza Khodarahimi #
#  﫥  Copyright     2024             #
#                                    #
######################################

# __SRCs.py
import os
import re
import sys
import time
import signal
import random
import logging
import datetime
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

import sys
import tkinter as tk
from tkinter import ttk
from io import StringIO
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

quantum = 1  # in seconds
frequency = 0.001
filename = '../input/Input.txt'
pdf_path = '../docs/Docs.pdf'

GUI = set()
Pid_Table = set()

def pid():
    while True:
        numb = random.randint(500, 1000)  # Assuming process IDs are between 1 and 1000
        if numb not in Pid_Table:
            Pid_Table.add(numb)            
            return numb

def priority():
    return random.randint(1,9)

# Function to redirect stdout to the Text widget
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
