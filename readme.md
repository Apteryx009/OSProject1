This program simulates different schedulers for OS Project 1.

Main.py holds the main part of the program, it's the file you run. 
usage: main.py [-h] {1,2,3,4} avg_arrival_rate avg_service_time quantum
main.py: error: the following arguments are required: scheduler, avg_arrival_rate, avg_service_time, quantum

Ex: 2 1 0.06 0.01
Notice that even for schedulers 1-3, we need the 4th argument of a quantum, this will be ignored by 1-3 but is nesssary nontheless. 

1: FCFS
2: SRTF
3: HRRN
4: Round Robin

run.py is like the bash file given in the promt, data generated from this is stored in data
NOTICE If you use this file, you will need to modify the file path

data/1 holds the data of each and every process (this is just for records not for actual execution)
data/2 holds the averages of the processes, it holds the average TAT per second, Total_Throughput Per Second ,CPU_Util (%), Avg Processses in_RQ

plotGeneralStats.py was used to generated the plots in pics


FCFS Scheduler Analysis:

    Average Processes in RQ: Noticeable peaks suggest periods of either bursty arrivals or instances where the system encountered compute-intensive tasks causing subsequent tasks to queue up.

    Average TAT (Sec): Peaks in TAT correlate with the increased queue length. It’s a clear indication of processes experiencing increased waiting times due to prior long-burst processes.

HRRN Scheduler Analysis:

    Average Throughput (Sec): Fluctuations highlight periods with a high density of processes possessing favorable Response Ratios, leading to rapid completions.

    Average Processes in RQ: Pronounced spikes hint at scenarios where the system received processes with closely matched Response Ratios, causing some delay in scheduling decisions.

    Average TAT (Sec): Peaks mirror the ready queue fluctuations. They signify moments when processes faced elongated waiting times, either due to closely matched Response Ratios or the presence of longer burst time processes.

SRTF Scheduler Analysis:

    Average Processes in RQ: We observe two pronounced spikes in the graph, notably in CSV files labeled "2-16" and "2-21". Such peaks in the ready queue can be indicative of either a sudden surge in process arrivals or the introduction of processes with longer burst times that are frequently interrupted by newly arriving processes with shorter burst times.

    Average Throughput (Sec): There's a substantial dip that seems to mirror the spikes in the ready queue, specifically around the "2-21" mark. The lowered throughput suggests that processes were being frequently preempted, causing a lag in their actual completion.

    Average CPU Utilization (%): The CPU utilization remains fairly constant and at the lower spectrum, with subtle peaks accompanying the spikes in the ready queue. A low CPU utilization in conjunction with high ready queue spikes hints that while there were many processes waiting, the CPU was often switching tasks instead of completing them, which is characteristic of preemptive scheduling with frequent context switches.

    Average TAT (Sec): TAT peaks coincide with the aforementioned spikes in the ready queue. Processes are likely waiting longer due to the preemptive nature of the scheduler, which may be exacerbated if there are frequent context switches without actual process completions.


Round Robin Scheduler (Quantum 0.01)
    Average Throughput: Appears to remain constant and low throughout the CSV files.
    Average CPU Utilization: Remains relatively constant and low.
    Average Processes in RQ (Run Queue): Consistently flat, indicating no fluctuation in the number of processes waiting in the run queue.
    Average TAT (Turnaround Time): Starts low but begins to rise sharply after a certain number of CSV files, indicating an increase in the time taken for processes to complete.

Round Robin Scheduler (Quantum 0.02)
    Average Throughput: Maintains a constant low value across the CSV files, similar to the 0.01 quantum chart.
    Average CPU Utilization: Again, remains quite constant and low.
    Average Processes in RQ: Just like the 0.01 quantum chart, this remains flat.
    Average TAT: Begins low and increases as more CSV files are processed, but the rise seems less steep compared to the 0.01 quantum chart.



