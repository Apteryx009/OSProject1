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

data/1 holds the data of each and every process (this is just for records not for actual execution)
data/2 holds the averages of the processes, it holds the average TAT per second, Total_Throughput Per Second ,CPU_Util (%), Avg Processses in_RQ

plotGeneralStats.py was used to generated the plots in pics



