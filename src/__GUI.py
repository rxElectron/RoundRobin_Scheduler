#!/bin/python3

######################################
#                                    #
#  @  filename    : __GUI.py         #
#    Developer   : Reza Khodarahimi #
#  﫥  Copyright     2024             #
#                                    #
######################################

# __GUI.py
from __SRCs import *
from __OS import *
from __IO import *

class ProcessExecutionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Execution Visualization")
        self.root.geometry("1200x500")
        self.root.configure(bg='white')

        self.top_frame = ttk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.btn_start_process = ttk.Button(self.top_frame, text="Start Process", command=self.start_process)
        self.btn_start_process.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_add_process = ttk.Button(self.top_frame, text="Add Process", command=self.add_process)
        self.btn_add_process.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_gnatt1 = ttk.Button(self.top_frame, text="Gnatt Chart", command=self.draw_gantt_chart)
        self.btn_gnatt1.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_retry = ttk.Button(self.top_frame, text="Docs", command=self.open_pdf)
        self.btn_retry.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_retry = ttk.Button(self.top_frame, text="Retry", command=self.retry_processes)
        self.btn_retry.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_exit = ttk.Button(self.top_frame, text="Exit", command=self.exit_application)
        self.btn_exit.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=1, column=0, sticky="nsew")

        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas.create_text(600, 25, text="﫥    Educational Free Usage | Reza Khodarahimi 𓀠 PGU", font=("Helvetica", 10), fill="black")

        self.output_text = tk.Text(self.frame, wrap="word", state="disabled", bg="khaki")
        self.output_text.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.output_text.tag_configure("default", foreground="#1B1A1A")
        self.output_text.tag_configure("info", foreground="#A3A3A3")
        self.output_text.tag_configure("printheader", foreground="#5F0033")
        self.output_text.tag_configure("processing", foreground="#9C0022")
        self.output_text.tag_configure("CPU", foreground="#5C005C")
        self.output_text.tag_configure("IO", foreground="#0000DB")
        self.output_text.tag_configure("resume", foreground="#59BAE0")
        self.output_text.tag_configure("pause", foreground="#E05959")
        self.output_text.tag_configure("message", foreground="#E7D9D9")
        self.output_text.tag_configure("warning", foreground="#CF8700")
        self.output_text.tag_configure("bypass", foreground="#A2CF00")
        self.output_text.tag_configure("error", foreground="#B30000")
        self.output_text.tag_configure("success", foreground="#008B00")

        self.text_redirector = TextRedirector(self.output_text)
        sys.stdout = self.text_redirector
        sys.stderr = TextRedirector(self.output_text, tag="error")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.processes = []
        self.execution_log = {}  # To log the execution time slices for each process // Gnatt usage

        self.os_instance = OS(self)
        self.update_gui()

    def update_gui(self):
        self.canvas.delete("all")
        self.draw_processes()
        self.root.after(1, self.update_gui)

    def draw_processes(self):
        self.canvas.create_text(200, self.canvas.winfo_height()-10, text="⌛ Priority Round Robin Scheduling | 﫥  Reza Khodarahimi 𓀠 2024", font=("Helvetica", 10), fill="gray")

        rect_width = 100
        rect_height = 50
        margin = 20
        max_processes_per_column = (self.canvas.winfo_height() - margin - 30) // (rect_height + margin)
        num_columns = (len(self.processes) + max_processes_per_column - 1) // max_processes_per_column

        total_height = (rect_height + margin) * max_processes_per_column
        total_width = num_columns * (rect_width + margin)

        # Adjust canvas size if needed
        current_height = self.canvas.winfo_height()
        current_width = self.canvas.winfo_width()

        if total_height > current_height or total_width > current_width:
            new_height = max(total_height, current_height)
            new_width = max(total_width, current_width)
            self.canvas.config(height=new_height, width=new_width)

        # Draw processes
        for i, process in enumerate(self.processes):
            col = i // max_processes_per_column
            row = i % max_processes_per_column
            x0 = 50 + col * (rect_width + margin)
            y0 = 50 + row * (rect_height + margin)
            x1 = x0 + rect_width
            y1 = y0 + rect_height
            color = self.get_color(process)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            if process.state == "Loading": 
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=f"{process.Name}\n{process.state} {process.clock_time}s")
            else: self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=f"{process.Name}\n{process.state}")

    def get_color(self, process):
        if process.is_complete:
            return "green"
        elif process.state == "Waiting":
            return "orange"
        elif process.state == "Terminated":
            return "pink"
        elif process.state == "Ready":
            return "yellow"
        elif process.state == "Loading":
            return "silver"
        elif process.state == "CPU":
            return "blue" 
        elif process.state == "IO":
            return "purple"
        else:
            return "red"

    def draw_gantt_chart(self):
        print_message(self.output_text,f"{self.execution_log}", "message")
        fig, ax = plt.subplots(figsize=(15, 8))

        color_map = {
            'CPU': 'blue',
            'IO': 'purple',
            'Waiting': 'orange',
            'Loading': 'silver',
            'Terminated': 'pink',
            'Ready': 'yellow',
            'Resumed': 'green',
            'Paused': 'red'
        }

        y_pos = 0
        yticks = []
        ytick_labels = []
        process_positions = {}
        process_end_times = {}

        for exec_id, (process_name, state) in self.execution_log.items():
            start_time = int(exec_id.replace('Execution', '')) - 1  # Assuming execution order as time
            duration = 1  # Assuming each execution step takes 1 time unit

            if process_name not in process_positions:
                process_positions[process_name] = y_pos
                yticks.append(y_pos)
                ytick_labels.append(process_name)
                process_end_times[process_name] = start_time + duration
                y_pos += 1
            else:
                last_end_time = process_end_times[process_name]
                if start_time > last_end_time:
                    waiting_start = last_end_time
                    waiting_duration = start_time - last_end_time
                    ax.broken_barh([(waiting_start, waiting_duration)], (process_positions[process_name] - 0.4, 0.8), facecolors=color_map['Waiting'])
                process_end_times[process_name] = start_time + duration

            ax.broken_barh([(start_time, duration)], (process_positions[process_name] - 0.4, 0.8), facecolors=color_map[state])

        ax.set_yticks(yticks)
        ax.set_yticklabels(ytick_labels)
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Gantt Chart of Processes Execution')

        # Create a legend
        legend_patches = [mpatches.Patch(color=color, label=action) for action, color in color_map.items()]
        ax.legend(handles=legend_patches, loc='upper right')

        plt.show()

    def start_process(self):
        self.thread = threading.Thread(target=self.Simulate, daemon=True)
        self.thread.start()

    def Simulate(self):
        processes = read_processes(filename, self)

        for process in processes:
            self.os_instance.add_process(process)
            process.Find_Behavior()
            process.Quantum()
            process.thread.start() # Start the thread for each process

        time_start = time.time()
        self.os_instance.run_round_robin() # Run processes in a round-robin fashion

        # Wait for all threads to finish
        for process in self.processes:
            process.thread.join()
        time_end = time.time()

        for process in self.processes:
            print_message(self.output_text,'----------------------------------------------------------------------------', "success")
            process.print_schedule()
            process.print_boolActions()
            print_message(self.output_text, f"Process {process.id} creation_time[creation_datetime]: {process.creation_datetime}", "error")
            print_message(self.output_text, f"Process {process.id} Response Time[response_time]: {process.response_time:.2f} seconds", "CPU")
            print_message(self.output_text, f"Process {process.id} Waiting Time[waiting_time]: {process.waiting_time:.2f} seconds", "IO")
            print_message(self.output_text, f"Process {process.id} Turnaround Time[turnaround_time]: {process.turnaround_time:.2f} seconds", "success")
            print_message(self.output_text, f"Process {process.id} ENDING Time[finish_datetime]: {process.finish_datetime} seconds", "warning")

        print_message(self.output_text,'----------------------------------------------------------------------------', "success")

        
        total_turnaround_time = time_end - time_start
        avg_turnaround_time = total_turnaround_time / len(self.processes)
        print_message(self.output_text, f"Average Turnaround Time: {avg_turnaround_time}", "IO")
        print_message(self.output_text, f"Total Turnaround Time: {total_turnaround_time}", "error")

    def add_process(self):
        self.os_instance.create_process(random.randint(1,3))

    def retry_processes(self):
        self.os_instance.RR_FLAG = False
        self.processes.clear()
        self.execution_log.clear()
        self.os_instance.RobinIndex = 1
        self.os_instance.processes.clear()
        self.canvas.delete("all")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        print_message(self.output_text, "Retrying the process simulation... [Auto]", "info")
        self.start_process()

    def open_pdf(self):
        main_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(pdf_path):
            subprocess.Popen(["xdg-open", pdf_path])  # Use xdg-open to open the PDF in Linux
        else:
            print("PDF file not found!")

    def exit_application(self):
        self.root.quit()
        self.root.destroy()
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)  # S
        # Exit Python interpreter
        exit()