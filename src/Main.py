#!/bin/python3

######################################
#                                    #
#  @  filename    : Main.py          #
#    Developer   : Reza Khodarahimi #
#  﫥  Copyright     2024             #
#                                    #
######################################

# Main.py
from __GUI import ProcessExecutionGUI
import tkinter as tk

def create_app():
    root = tk.Tk()
    app = ProcessExecutionGUI(root)
    root.mainloop()
    # while True : pass

if __name__ == '__main__':
    create_app()
