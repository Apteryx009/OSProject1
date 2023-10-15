import csv
import os
import matplotlib.pyplot as plt
import re
import pandas as pd
import glob
def compute_averages(filepath):
    TATs = []
    Throughputs = []
    CPU_utils = []
    Avg_procs = []

    with open(filepath, "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip the header
        
        for row in csv_reader:
            TATs.append(float(row[0]))
            Throughputs.append(float(row[1]))
            CPU_utils.append(float(row[2]))
            Avg_procs.append(float(row[3]))

    return sum(TATs)/len(TATs), sum(Throughputs)/len(Throughputs), sum(CPU_utils)/len(CPU_utils), sum(Avg_procs)/len(Avg_procs)

def custom_sort(filename):
    parts = filename.split('-')
    return int(parts[0]), int(parts[1])


def plot_scheduler(scheduler_files, scheduler_name):
    files = []
    avg_TATs = []
    avg_Throughputs = []
    avg_CPU_utils = []
    avg_Avg_procs = []

    for filename, filepath in scheduler_files:
        avg_TAT, avg_Throughput, avg_CPU_util, avg_Avg_proc = compute_averages(filepath)
        match = re.search(r"(\d+-\d+)", filename)
        if match:
            files.append(match.group(1))
        else:
            files.append(filename)
        avg_TATs.append(avg_TAT)
        avg_Throughputs.append(avg_Throughput)
        avg_CPU_utils.append(avg_CPU_util)
        avg_Avg_procs.append(avg_Avg_proc)
    
    files = sorted(files, key=custom_sort)
    
    # Plotting
    fig, ax1 = plt.subplots(figsize=(15, 10))

    # Different line styles for each metric
    ax1.plot(files, avg_Throughputs, 'g-', label='Average Throughput (Sec)')
    ax1.plot(files, avg_CPU_utils, 'r--', label='Average CPU Utilization (%)')
    ax1.plot(files, avg_Avg_procs, 'o-', color='orange', label='Average Processes in RQ')
    
    ax2 = ax1.twinx()
    ax2.plot(files, avg_TATs, 'b-.', label='Average TAT (Sec)')
    
    ax1.set_xlabel('CSV Files')
    ax1.set_ylabel('Values')
    ax1.legend(loc='upper left')

    ax2.set_ylabel('Average TAT')
    ax2.legend(loc='upper right')

    plt.title(f"{scheduler_name} Scheduler")
    
    ax1.tick_params(axis='x', rotation=45)
    
    fig.tight_layout()
    plt.show()



# Directory containing the CSV files
directory = "C:/Users/jacob\Documents/Coding/osProjectMINE/data/2/"  

schedulers = {
    "1-": "FCFS",
    "2-": "SRTF",
    "3-": "HRRN"
}

for prefix, name in schedulers.items():
    scheduler_files = [(filename, os.path.join(directory, filename)) for filename in os.listdir(directory) if filename.startswith(prefix) and filename.endswith('.csv')]
    plot_scheduler(scheduler_files, name)




# Fetch all files with 'quatum' in their name
file_list = sorted(glob.glob(os.path.join(directory, "*quatum*.csv")))
print(file_list)

def extract_quantum_and_date(filename):
    match = re.search(r"(\d+-\d+)-(\d+quatumIS)(0\.\d+)", filename)
    if match:
        return match.groups()[2], match.groups()[0]
    return None, None

def extract_quantum(filename):
    match = re.search(r"(\d+quatumIS)(0\.\d+)", filename)
    if match:
        return match.groups()[1]
    return None

# Group the files based on their quantum value
quantum_groups = {}
for file in file_list:
    quantum, date = extract_quantum_and_date(file)
    if quantum not in quantum_groups:
        quantum_groups[quantum] = []
    quantum_groups[quantum].append((date, file))

# Sort each group by date and plot them separately
for quantum, files in quantum_groups.items():
    sorted_files = sorted(files, key=lambda x: custom_sort(x[0]))
    print(f"Plotting for quantum {quantum}")
    plot_scheduler(sorted_files, f"Round Robin Scheduler (Quantum {quantum})")
