
# Speedtest Script

## Description
This Python script automates running the `speedtest` command multiple times and calculates the average download and upload speeds. Additionally, it measures and reports network latency, jitter, and high/low values for each run. The script also plots the download and upload speeds, along with their linear regression lines, to visually represent the data.

## Requirements
- Python 3
- `speedtest-cli` command-line tool
- Python libraries: `numpy`, `matplotlib`

## Installation
1. **Install Python 3:**
   Ensure Python 3 is installed on your system.

2. **Install Required Python Libraries:**
   Use pip to install the required Python libraries:
   ```bash
   pip install numpy matplotlib
   ```

3. **Install `speedtest-cli`:**
   The `speedtest-cli` tool must be installed and accessible from the command line.

## Usage
Run the script from the command line, specifying the number of times you want to run the `speedtest` command:

```bash
python speedtest.py <number_of_runs>
```

Replace `<number_of_runs>` with the number of times you want to execute the speed test.

## Features
- **Multiple Test Runs:** The script automates running the `speedtest` command a specified number of times.
- **Speed Analysis:** Calculates and displays the average download and upload speeds across all runs.
- **Network Metrics:** Measures and reports additional network metrics like latency, jitter, and high/low values.
- **Data Visualization:** Plots the download and upload speeds for each run, along with linear regression lines, using `matplotlib`.
- **Command-Line Arguments:** Allows specifying the number of test runs directly as a command-line argument.
- **Formatted Output:** Presents all data in a clear, readable format in the console.

---

