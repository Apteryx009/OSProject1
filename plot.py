import csv
import matplotlib.pyplot as plt

# Extract data from CSV input
processes = []
burst_times = []
arrival_times = []
time_of_first_services = []
completion_times = []
waiting_times = []
turnaround_times = []

with open("stats.csv", "r") as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # skip the header
    for row in csv_reader:
        processes.append(int(row[0]))
        burst_times.append(float(row[1]))
        arrival_times.append(float(row[2]))
        time_of_first_services.append(float(row[3]))
        completion_times.append(float(row[4]))
        waiting_times.append(float(row[5]))
                                #CT          -     AT
        turnaround_times.append(abs(float(row[4]) -float(row[2])))

# Plotting Turnaround Time
plt.figure(figsize=(12, 7))
plt.bar(processes, turnaround_times, color='cyan')
plt.title("Turnaround Time for each Process")
plt.xlabel("Process ID")
plt.ylabel("Turnaround Time")
plt.xticks(processes)
plt.tight_layout()
plt.savefig('turnaround_times.png')
plt.show()


# Plotting Burst Time
plt.figure(figsize=(12, 7))
plt.bar(processes, burst_times, color='blue')
plt.title("Burst Time for each Process")
plt.xlabel("Process ID")
plt.ylabel("Burst Time")
plt.xticks(processes)
plt.tight_layout()
plt.savefig('burst_times.png')
plt.show()

# Plotting Arrival Time
plt.figure(figsize=(12, 7))
plt.bar(processes, arrival_times, color='green')
plt.title("Arrival Time for each Process")
plt.xlabel("Process ID")
plt.ylabel("Arrival Time")
plt.xticks(processes)
plt.tight_layout()
plt.savefig('arrival_times.png')
plt.show()

# Plotting Time of First Service
plt.figure(figsize=(12, 7))
plt.bar(processes, time_of_first_services, color='yellow')
plt.title("Time of First Service for each Process")
plt.xlabel("Process ID")
plt.ylabel("Time of First Service")
plt.xticks(processes)
plt.tight_layout()
plt.savefig('time_of_first_services.png')
plt.show()

# Plotting Completion Time
plt.figure(figsize=(12, 7))
plt.bar(processes, completion_times, color='red')
plt.title("Completion Time for each Process")
plt.xlabel("Process ID")
plt.ylabel("Completion Time")
plt.xticks(processes)
plt.tight_layout()
plt.savefig('completion_times.png')
plt.show()

# Plotting Waiting Time
plt.figure(figsize=(12, 7))
plt.bar(processes, waiting_times, color='purple')
plt.title("Waiting Time for each Process")
plt.xlabel("Process ID")
plt.ylabel("Waiting Time")
plt.xticks(processes)
plt.tight_layout()
plt.savefig('waiting_times.png')
plt.show()
