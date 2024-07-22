#!/bin/python3

######################################
#                                    #
#  @  filename    : __OS.py          #
#    Developer   : Reza Khodarahimi #
#  﫥  Copyright     2024             #
#                                    #
######################################

# __OS.py
from __IO import *
from __SRCs import *
from __PROCESS import *

class OS():
    def __init__(self, gui):
        self.Name = 'X - OS'
        self.lock = threading.Lock()
        self.gui = gui
        self.quantum = quantum
        self.processes = gui.processes
        self.is_pause = threading.Event()
        threading.Event.clear(self.is_pause)
        self.RR_FLAG = False
        self.lock = threading.Lock()  # Add a lock for synchronization
        self.Robin_Current_Index = 0
        self.RobinIndex = 1

    def create_process(self, threshold):
        process = PROCESS(self.gui)
        process.clock_time = threshold
        self.add_process(process)

        def create(process):
            # process.CPU = [0, 4, 5]
            # process.IO = [2]
            self.analyse(process)
            print(process.CPU)
            print(process.IO)
            process.Find_Behavior()
            process.Quantum()
            print_message(self.gui.output_text,f"[NEW] Process {process.id} created at {process.creation_datetime}","error",)
            if self.RR_FLAG:
                process.thread.start()

        timer = threading.Timer(threshold, create, args=[process])
        timer.start()
        
    def add_process(self, process):
        with self.lock:
            if process not in self.processes:
                self.gui.processes.append(process)
                print_message(self.gui.output_text, f"Added process {process.id}", "processing")
            else:
                print_message(self.gui.output_text, f"Process {process.id} already exists in the list.", "warning")

    def remove_process(self, process):
        with self.lock:
            try:
                self.processes.remove(process)
                print_message(self.gui.output_text, f"Removed process {process.id}", "processing")
            except ValueError:
                print_message(self.gui.output_text, f"Process {process.id} not found in the list.", "info")

    def run_round_robin(self):
        def round_robin():
            print_message(self.gui.output_text, "----------------------------------------------------------------------------\n\t\t\tStarting round-robin scheduling...\n----------------------------------------------------------------------------", "success")
            while self.processes:
                with self.lock:
                    # Sort processes by priority before each round
                    self.processes.sort(key=lambda x: x.priority)
                    process = self.processes[self.Robin_Current_Index]
                    self.Robin_Current_Index = (self.Robin_Current_Index + 1) % len(self.processes)
                
                if not process.is_complete:
                    process.turn.set()
                    self.resume(process)
                    print_message(self.gui.output_text, f"Process {process.id} resumed.", "resume")
                    self.gui.execution_log[f"Execution{self.RobinIndex}"] = f"{process.Name}", f"{process.state}"
                    self.RobinIndex += 1
                    process.turn.wait(timeout=self.quantum)  # Run for a quantum time
                    process.turn.clear()
                    self.pause(process)
                    print_message(self.gui.output_text, f"Process {process.id} paused.", "pause")
                else:
                    print_message(self.gui.output_text, f"Process {process.id} is already complete.", "bypass")
                
                if all(p.is_complete for p in self.processes):
                    self.Robin_Current_Index = 0
                    break

            print_message(self.gui.output_text, "----------------------------------------------------------------------------\n\t\t\tRound-robin scheduling completed.\n----------------------------------------------------------------------------", "info")

        threading.Thread(target=round_robin, daemon=True).start()
        self.RR_FLAG = True
        self.utils()


    def print_schedule(self, process):

        try:
            process.print_schedule()
        except Exception as e:
            print_message(self.gui.output_text, f"{e}", "error")

    def print_boolActions(self, process):

        try:
            process.print_boolActions()
        except Exception as e:
            print_message(self.gui.output_text, f"{e}", "error")

    def resume(self, process):
        with self.lock:
            try:
                process.resume()
            except Exception as e:
                print_message(self.gui.output_text, f"{e}", "error")

    def pause(self, process):
        with self.lock:
            try:
                process.pause()
            except Exception as e:
                print_message(self.gui.output_text, f"{e}", "error")
                
    def analyse(self, process):
        num_list = sorted(random.sample(range(31), random.randint(10, 12)))
        if num_list[0] != 0 : num_list[0] = 0
        if random.random() < 0.5:
            CPU, IO = num_list[1::2], num_list[::2]
        else:
            """
            Assigns the even-indexed elements of `num_list` to `CPU` and the odd-indexed elements to `IO`.
            This is a helper function used within the `numbering()` function to randomly generate CPU and IO burst times for a new process.
            """
            CPU, IO = num_list[::2], num_list[1::2]
        process.CPU = CPU
        process.IO = IO

    def utils(self):
        """
        Utility functions for the OS simulation.

        The `utils()` method starts two background threads:

        1. `listen_printer()` thread:
           - Iterates through the `self.processes` list.
           - If a process has not printed its boolean actions yet (`p.first_print`), it calls `p.print_boolActions()` to print the process's boolean actions.
           - Sleeps for `self.quantum` seconds before the next iteration.

        2. `listen_queue()` thread:
           - Acquires the `self.lock` lock.
           - Sorts the `self.processes` list by priority.
           - Sleeps for `self.quantum` seconds before the next iteration.

        These utility functions help manage the state of the OS simulation, such as printing process information and maintaining the priority queue of processes.
        """
        def listen_printer():
            while True:
                for p in self.processes:
                    if not p.first_print:
                        p.print_boolActions()
                time.sleep(self.quantum)

        printer_thread = threading.Thread(target=listen_printer)
        printer_thread.start()

        def listen_queue():
            while True:
                with self.lock:
                    self.processes.sort(key=lambda x: (x.priority))
                time.sleep(self.quantum)

        thread_queue = threading.Thread(target=listen_queue)
        thread_queue.start()
