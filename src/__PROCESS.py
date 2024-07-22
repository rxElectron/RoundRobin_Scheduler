#!/bin/python3

######################################
#                                    #
#  @  filename    : __PROCESS.py     #
#    Developer   : Reza Khodarahimi #
#  﫥  Copyright     2024             #
#                                    #
######################################

# __PROCESS.py
from __SRCs import *
from __OS import *
from __IO import *

class PROCESS():
    def __init__(self, gui):
        """
        Initialize a new PROCESS instance.
        """
        self.id = pid()  # Call the `pid()` function to generate a unique process ID
        self.priority = priority()
        self.Name = f"P{self.id}({self.priority})"
        self.thread = threading.Thread(target=self.run)
        self.pause_event = threading.Event()
        self.pause_event.set()  # Start in a paused state
        self.CPU = []
        self.IO = []
        self.behave = {}
        self.actArray = []
        self.is_complete = False
        self.start_time = 0
        self.finish_time = 0
        self.response_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.paused_time = 0
        self.clock_time = 0
        self.creation_time = time.time()
        self.creation_datetime = datetime.datetime.fromtimestamp(self.creation_time).strftime('%Y-%m-%d %H:%M:%S')
        self.gui = gui
        self.quantum = quantum
        self.finish_time = 0
        self.finish_datetime = 0
        self.turn = None
        self.state = "Loading"
        self.first_print = False
        self.turn = threading.Event()  # Initialize turn as a threading Event
        self.stepcounter = 1

    def run(self):
        """
        Simulate the process execution.
        """
        while not self.is_complete:
            self.state = "Waiting"
            self.pause_event.wait()  # Block until the event is cleared (resume is called)
            self.start_time = time.time()  # Record the start time of execution
            self.response_time = self.start_time - self.creation_time
            self.waiting_time = self.response_time

            for action in self.actArray:
                if self.is_complete:
                    break
                self.state = "Waiting"
                self.pause_event.wait()  # Ensure we are not paused
                self.turn.wait()
                self.turn.clear()
                action_type = 'CPU' if action else 'IO'
                self.state = action_type
                print_message(self.gui.output_text, f"Executing {self.Name} for a quantum of {action_type} action in step {self.stepcounter}", action_type)
                logging.info(f"Executing {self.Name} for a quantum of {action_type} action in step {self.stepcounter}")
                # Add logic to mark the process as complete when done
                time.sleep(self.quantum)  # Simulate the execution for a quantum
                self.turn.set()
                self.state = "Terminated"
                self.stepcounter += 1
                time.sleep(frequency)

            self.pause_event.wait()  # Ensure we are not paused
            self.state = "Terminated"
            self.is_complete = True  # Mark the process as complete after one execution
            self.finish_time = time.time()  # Record the finish time of execution
            self.finish_datetime = datetime.datetime.fromtimestamp(self.finish_time).strftime('%Y-%m-%d %H:%M:%S')
            self.turnaround_time = self.finish_time - self.creation_time

    def Find_Behavior(self):
        """
        Determine the process behavior based on CPU and IO bursts.
        """
        current_time = 0
        schedule_index = 1
        max_length = max(len(self.CPU), len(self.IO))

        if self.CPU and self.CPU[0] == 0:
            for i in range(max_length):
                if i < len(self.CPU) - 1:
                    cpu_start = self.CPU[i]
                    cpu_end = self.IO[i] if i < len(self.IO) else self.CPU[i + 1]
                    cpu_time = cpu_end - cpu_start
                    cpu_schedule_key = f"PID[{self.id}]_STEP{schedule_index}_cpu"
                    self.behave[cpu_schedule_key] = {'time': (current_time, current_time + cpu_time), 'type': 'CPU'}
                    current_time += cpu_time
                    schedule_index += 1

                if i < len(self.IO):
                    io_start = self.IO[i]
                    io_end = self.CPU[i + 1] if i + 1 < len(self.CPU) else io_start
                    io_time = io_end - io_start
                    io_schedule_key = f"PID[{self.id}]_STEP{schedule_index}_io"
                    self.behave[io_schedule_key] = {'time': (current_time, current_time + io_time), 'type': 'IO'}
                    current_time += io_time
                    schedule_index += 1

        elif self.IO and self.IO[0] == 0:
            for i in range(max_length):
                if i < len(self.IO):
                    io_start = self.IO[i]
                    io_end = self.CPU[i] if i < len(self.CPU) else io_start
                    io_time = io_end - io_start
                    io_schedule_key = f"PID[{self.id}]_STEP{schedule_index}_io"
                    self.behave[io_schedule_key] = {'time': (current_time, current_time + io_time), 'type': 'IO'}
                    current_time += io_time
                    schedule_index += 1

                if i < len(self.CPU) - 1:
                    cpu_start = self.CPU[i]
                    cpu_end = self.IO[i + 1] if i + 1 < len(self.IO) else self.CPU[i + 1]
                    cpu_time = cpu_end - cpu_start
                    cpu_schedule_key = f"PID[{self.id}]_STEP{schedule_index}_cpu"
                    self.behave[cpu_schedule_key] = {'time': (current_time, current_time + cpu_time), 'type': 'CPU'}
                    current_time += cpu_time
                    schedule_index += 1

    def Quantum(self):
        """
        Convert the CPU and IO bursts into time slices (quanta) for round-robin scheduling.
        """
        max_length = max(len(self.CPU), len(self.IO))

        if self.CPU and self.CPU[0] == 0:
            for i in range(max_length):
                if i < len(self.CPU) - 1:
                    cpu_start = self.CPU[i]
                    cpu_end = self.IO[i] if i < len(self.IO) else self.CPU[i + 1]
                    cpu_time = cpu_end - cpu_start
                    repeat = int(cpu_time / quantum)
                    for _ in range(repeat):
                        self.actArray.append(True)

                if i < len(self.IO):
                    io_start = self.IO[i]
                    io_end = self.CPU[i + 1] if i + 1 < len(self.CPU) else io_start
                    io_time = io_end - io_start
                    repeat = int(io_time / quantum)
                    for _ in range(repeat):
                        self.actArray.append(False)
            self.state = "Ready"

        elif self.IO and self.IO[0] == 0:
            for i in range(max_length):
                if i < len(self.IO):
                    io_start = self.IO[i]
                    io_end = self.CPU[i] if i < len(self.CPU) else io_start
                    io_time = io_end - io_start
                    repeat = int(io_time / quantum)
                    for _ in range(repeat):
                        self.actArray.append(False)

                if i < len(self.CPU) - 1:
                    cpu_start = self.CPU[i]
                    cpu_end = self.IO[i + 1] if i + 1 < len(self.IO) else self.CPU[i + 1]
                    cpu_time = cpu_end - cpu_start
                    repeat = int(cpu_time / quantum)
                    for _ in range(repeat):
                        self.actArray.append(True)
            self.state = "Ready"


    def print_schedule(self):
        """
        Print the schedule of behavior for the process.
        """
        print_message(self.gui.output_text, f"Schedule of behavior [Process {self.Name}]:", "printheader")
        for key, value in self.behave.items():
            print_message(self.gui.output_text, f"{key}: {value}", "info")

    def print_boolActions(self):
        """
        Print the boolean actions of the process.
        """
        if not self.first_print:
            self.first_print = True
            print_message(self.gui.output_text, f"Booleans of Actions [Process {self.id}]:", "printheader")
            print_message(self.gui.output_text, f"{self.actArray}", "info")

    def pause(self):
        """
        Pause the process.
        """
        self.state = "Paused"
        logging.info(f"Pausing process {self.Name}")
        self.pause_event.clear()
        self.paused_time = time.time()
        if self.is_complete : self.state = "Terminated"

    def resume(self):
        """
        Resume the process.
        """
        self.state = "Resumed"
        logging.info(f"Resuming process {self.Name}")
        self.pause_event.set()
        if self.paused_time > 0:
            # If the process was paused before, calculate the waiting time
            timeDuration = time.time() - self.paused_time
            self.waiting_time += timeDuration
            self.paused_time = 0  # Reset paused_time for future pauses