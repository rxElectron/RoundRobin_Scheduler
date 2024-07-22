
#Round Robin Process Scheduler

This project simulates process scheduling using the Round Robin algorithm. The simulation includes process creation, execution, and visualization.

## Project Structure

| Directory   | Content                                         |
|-------------|-------------------------------------------------|
| `docs/`     | Project documentation                           |
| `src/`      | Source code files                               |
| `input/`    | Input files for the simulation                  |
| `.gitignore`| Specifies files to ignore in the repository     |
| `LICENSE`   | Project license                                 |
| `README.md` | Project overview and instructions               |

## Description

This project simulates process scheduling using the Round Robin algorithm. The simulation manages multiple processes, each with specified CPU and I/O times. The processes are executed and visualized using a graphical user interface.

### Key Features

| Feature                 | Description                                                            |
|-------------------------|------------------------------------------------------------------------|
| Process Scheduling      | Implements the Round Robin scheduling algorithm for process management.|
| Graphical Visualization | Real-time graphical interface to visualize process states and execution.|
| Detailed Metrics        | Reports process metrics such as waiting time, response time, and turnaround time.|

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/OS_Project.git
   cd OS_Project
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the simulation:**

   Navigate to the `src` directory and execute the `Main.py` script.

   ```bash
   cd src
   python Main.py
   ```

2. **Input File:**

   The `input/Input.txt` file contains the initial processes with their respective CPU and I/O times.

3. **Graphical User Interface:**

   The GUI allows you to start, add, and retry processes. It also displays the Gantt chart for process execution.

## Files and Classes

| File           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `src/__SRCs.py`| Contains auxiliary functions and standard libraries.                         |
| `src/__PROCESS.py` | Defines the `PROCESS` class, which simulates each process with attributes like ID, priority, and execution behavior. |
| `src/__IO.py`  | Handles reading process input from a text file and includes the `TextRedirector` class to manage output redirection. |
| `src/__OS.py`  | Implements the `OS` class for process management, including adding, removing, and running processes using Round Robin scheduling. |
| `src/__GUI.py` | Provides a graphical user interface for the simulation, utilizing `tkinter` and `threading` for real-time updates. |
| `src/Main.py`  | The main entry point of the program, which initializes and runs the application. |

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact [Your Name] at [Your Email].

## Acknowledgments

- Thank you to all contributors and open-source projects that made this project possible.
