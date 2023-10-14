import csv
import os
import matplotlib.pyplot as plt
import re

def compute_averages(filepath):
    TATs = []
    WTs = []

    with open(filepath, "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip the header
        
        for row in csv_reader:
            completion_time = float(row[4])
            arrival_time = float(row[2])
            waiting_time = float(row[5])
            
            TAT = completion_time - arrival_time
            
            TATs.append(TAT)
            WTs.append(waiting_time)

    return sum(TATs)/len(TATs), sum(WTs)/len(WTs)


def custom_sort(filename):
    parts = filename.split('-')
    return int(parts[0]), int(parts[1])

def plot_scheduler(scheduler_files, scheduler_name):
    files = []
    avg_TATs = []
    avg_WTs = []

    for filename, filepath in scheduler_files:
        avg_TAT, avg_WT = compute_averages(filepath)
        # Extract the "X-Y" format from the filename
        match = re.search(r"(\d+-\d+)", filename)
        if match:
            files.append(match.group(1))
        else:
            files.append(filename)
        avg_TATs.append(avg_TAT)
        avg_WTs.append(avg_WT)
    
    files = sorted(files, key=custom_sort)
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(files, avg_TATs, 'g-')
    ax2.plot(files, avg_WTs, 'b--')
    ax1.set_xlabel('CSV Files')
    ax1.set_ylabel('Average TAT', color='g')
    ax2.set_ylabel('Average Waiting Time (dashed line)', color='b')
    ax1.set_title(f"{scheduler_name} Scheduler")
    plt.show()

# Directory containing the CSV files
directory = "C:/Users/jacob\Documents/Coding/osProjectMINE/data/1/"  

schedulers = {
    "1-": "FCFS",
    "2-": "SRTF",
    "3-": "HRRN",
    "4-": "RR"
}

for prefix, name in schedulers.items():
    scheduler_files = [(filename, os.path.join(directory, filename)) for filename in os.listdir(directory) if filename.startswith(prefix) and filename.endswith('.csv')]
    plot_scheduler(scheduler_files, name)
