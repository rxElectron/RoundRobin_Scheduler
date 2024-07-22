
# 🌀 Round Robin Process Scheduler

This project simulates process scheduling using the Round Robin algorithm. The simulation includes process creation, execution, and visualization.

## 📁 Project Structure

| Directory      | Content                                         |
|----------------|-------------------------------------------------|
| `docs/`        | 📄 Project documentation                        |
| `src/`         | 📂 Source code files                            |
| `input/`       | 📑 Input files for the simulation               |
| `.gitignore`   | 🚫 Specifies files to ignore in the repository  |
| `LICENSE`      | ⚖️ Project license                              |
| `README.md`    | 📜 Project overview and instructions            |

## 📜 Description

This project simulates process scheduling using the Round Robin algorithm. The simulation manages multiple processes, each with specified CPU and I/O times. The processes are executed and visualized using a graphical user interface.

### ✨ Key Features

| Feature                 | Description                                                            |
|-------------------------|------------------------------------------------------------------------|
| 🕹️ Process Scheduling   | Implements the Round Robin scheduling algorithm for process management.|
| 📊 Graphical Visualization | Real-time graphical interface to visualize process states and execution.|
| 📈 Detailed Metrics     | Reports process metrics such as waiting time, response time, and turnaround time.|

## 💾 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/therboy/RoundRobin_Scheduler.git
   cd RoundRobin_Scheduler
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements.txt --break-system-packages
   ```

### 🛠️ Additional Setup for `tkinter`

You cannot install `tkinter` using `pip` because it is not available as a standalone package. Instead, it comes bundled with Python installations. Here’s how you can ensure you have it:

#### For Different Operating Systems

- **Windows:**
  Tkinter is included with the standard Python installation. If you installed Python from the official installer, you should already have it.

- **Ubuntu/Debian:**
  You can install Tkinter with:
  ```bash
  sudo apt-get install python3-tk
  ```

- **Fedora:**
  Use the following command:
  ```bash
  sudo dnf install python3-tkinter
  ```

- **macOS:**
  Tkinter is usually included with the Python installation from python.org. If you installed Python via Homebrew, you might need to install it separately:
  ```bash
  brew install python-tk
  ```

### 🧪 Verify Installation

To check if Tkinter is installed correctly, run:

```python
import tkinter
tkinter._test()
```

If a small window appears, Tkinter is working.

## 🚀 Usage

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

## 🗂️ Files and Classes

| File               | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `src/__SRCs.py`    | 📚 Contains auxiliary functions and standard libraries.                     |
| `src/__PROCESS.py` | 🏭 Defines the `PROCESS` class, which simulates each process with attributes like ID, priority, and execution behavior. |
| `src/__IO.py`      | 📥 Handles reading process input from a text file and includes the `TextRedirector` class to manage output redirection. |
| `src/__OS.py`      | 🖥️ Implements the `OS` class for process management, including adding, removing, and running processes using Round Robin scheduling. |
| `src/__GUI.py`     | 🖼️ Provides a graphical user interface for the simulation, utilizing `tkinter` and `threading` for real-time updates. |
| `src/Main.py`      | 🚪 The main entry point of the program, which initializes and runs the application. |

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any questions or inquiries, please contact Reza Khodarahimi at kh.reza10@gmail.com.

## 🙏 Acknowledgments

- Thank you to all contributors and open-source projects that made this project possible.
