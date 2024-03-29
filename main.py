import heapq  #
import csv
import argparse
import random
#import psutil
from Event import Event
from FCFS import FCFS
from SRTF import SRTF
from HRRN import HRRN
from RR import RR


def write_processes_to_csv(processes, filename):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['Process ID', 'Burst Time', 'Arrival Time', 'Time of First Service',
                      'Completion Time', 'Waiting Time']  # Add other field names as needed
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the column headers
        for process in processes:
            writer.writerow(process.to_dict())


def write_generalStats_to_csv(TAT, Total_Throughput, CPU_Util, AvgPInRQ):
    with open("generalStats.csv", 'w', newline='') as file:
        fieldnames = ['Avg_TAT', 'Avg_Throughput', 'CPU_Util', 'Avg_Proc_in_RQ']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write the column headers
        
        # Create a dictionary with the data
        data = {
            'Avg_TAT': TAT,
            'Avg_Throughput': Total_Throughput,
            'CPU_Util': CPU_Util,
            'Avg_Proc_in_RQ': AvgPInRQ
        }
        
        writer.writerow(data)



class Process:
    def __init__(self, process_id, AT, BT):
        self.process_id = process_id
        self.BT = BT
        self.BTLeft = BT
        self.AT = AT
        self.TimeOf1stService = None
        self.CT = None
        self.WT = 0
        self.LastPreempted = None
        self.TAT = None

    # If add more attributes to the Process class, make sure to update this method accordingly

    def to_dict(self):
        return {
            'Process ID': self.process_id,
            'Burst Time': self.BT,
            'Arrival Time': self.AT,
            'Time of First Service': self.TimeOf1stService,
            'Completion Time': self.CT,
            'Waiting Time': self.WT
            # ... add other attributes as needed ...
        }

def write_events_to_file(event_list, filename="sampleEvents.txt"):
    with open(filename, 'w') as file:
        # Writing a header for better readability
        file.write("Time\tType\tProcess\n")
        file.write("-------------------------\n")
        
        for event in event_list:
            event_type = ""
            
            if event.type == 1:
                event_type = "arrival"
            elif event.type == 2:
                event_type = "departure"
            elif event.type == 3:
                event_type = "swapping"
            else:
                event_type = "unknown"
            
            file.write(f"{event.time}\t{event_type}\t{event.Process}\n")



class SimulationClock:
    def __init__(self, avg_arrival_rate, avg_service_time):
        self.current_time = 0.0
        self.event_queue = []
        self.ready_queue = []
        self.avg_arrival_rate = avg_arrival_rate
        self.avg_service_time = avg_service_time
        self.latestPID = 0
        self.processed_processes = 0
        self.allP = []
        self.total_processes = 0
        self.TotalExecutedTime = 0
        self.totalIdle = 0
        self.integral_ready_queue = 0.0
        self.last_event_time = 0.0
        self.sum_ready_queue_lengths = 0.0
        self.total_duration_weighted = []

  
        

    def run(self, total_processes, scheduler, q):
        #print(len(self.ready_queue))
        self.total_processes = total_processes

        def createNewP():
            inter_arrival_time = random.expovariate(self.avg_arrival_rate)
            BT_Time = random.expovariate(1.0 / self.avg_service_time)
            self.latestPID += 1
            if len(self.allP) > 0:  # changed condition to check if any processes exist
                # this will make arrival time dynamic
                AT_Time = self.allP[-1].AT + inter_arrival_time
            else:
                # the first process can just have inter_arrival_time as its arrival time
                AT_Time = inter_arrival_time
            newP = Process(self.latestPID, AT_Time, BT_Time)
            return newP

        while self.processed_processes < total_processes:
            # Continue to schedule processes until total_processes have been processed

            if len(self.allP) < total_processes:
                
                the_new_p = createNewP()
                newEvent = Event(the_new_p, self.current_time, 1)
                self.event_queue.append(newEvent)
                self.ready_queue.append(the_new_p)
                self.ready_queue.sort(key=lambda p: p.AT)


                # Append the_new_p, not the_first_p
                self.allP.append(the_new_p)
            if scheduler == "FCFS":
                # print("Chosen FCFS")
                FCFS(self)
            elif scheduler == "SRTF":
                # print("Chosen SRTF")
                SRTF(self)
            elif scheduler == "HRRN":
                # print("Chosen HRRN")
                HRRN(self)
            elif scheduler == "RR":
                # print("Chosen RR")
                RR(self, q)
            
            #print(len(self.ready_queue))

            # FCFS(self)
            # SRTF(self)
            # HRRN(self)
            # RR(self, self.allP, 1)
            # print(self.current_time, len(self.allP), self.processed_processes)

        # sim is done
         # metric stuff
        # figure out total excututation time

        total_exec = 0.0
        Completed = 0
        totalTAT = 0
        for process in self.allP:
            if process.CT != None:
                process.TAT = abs(process.CT - process.AT)
                totalTAT += process.TAT
                Completed += 1
                total_exec += process.BT

        print(total_exec, " total execution time")
        throughput = self.processed_processes / self.current_time
        print("The throughput is ", throughput)
        total_cpu_time = self.totalIdle + total_exec
        print(total_cpu_time, total_exec, self.totalIdle)
        cpu_util = (total_exec / total_cpu_time) 
        print("CPU UTIL: ", cpu_util, "%")
        #average_processes_in_ready_queue = self.integral_ready_queue / self.current_time
        #print("Avg process in RQ: ", average_processes_in_ready_queue)
        avgTAT = totalTAT / Completed
        print("Average TAT ", avgTAT )

        Avg_proccesses_in_rq = cpu_util / (1 - cpu_util) - cpu_util
        print("Avg processes in RQ", Avg_proccesses_in_rq)
       
        write_events_to_file(self.event_queue)
        
       

        write_generalStats_to_csv(avgTAT, throughput, cpu_util, Avg_proccesses_in_rq)
        write_processes_to_csv(self.allP, 'stats.csv')


# For user input
parser = argparse.ArgumentParser(description="Process Scheduling Simulator")
parser.add_argument("scheduler", type=int, choices=[
                    1, 2, 3, 4], help="Scheduler type (1=FCFS, 2=SRTF, 3=HRRN, 4=RR)")
parser.add_argument("avg_arrival_rate", type=float,
                    help="Average arrival rate (lambda)")
parser.add_argument("avg_service_time", type=float,
                    help="Average service time")
parser.add_argument("quantum", type=float, default=1.0,
                    help="Time quantum for RR scheduler (default: 1.0)")

args = parser.parse_args()
scheduler = ""
if args.scheduler == 1:
    print("Selected Scheduler: FCFS")
    scheduler = "FCFS"
elif args.scheduler == 2:
    print("Selected Scheduler: SRTF")
    scheduler = "SRTF"
elif args.scheduler == 3:
    print("Selected Scheduler: HRRN")
    scheduler = "HRRN"
elif args.scheduler == 4:
    print("Selected Scheduler: RR")
    scheduler = "RR"

avg_arrival_rate = args.avg_arrival_rate
avg_service_time = args.avg_service_time
quantum = 1  # default
quantum = args.quantum
print(quantum)


total_processes = 10000  # Adjust this as needed

# Simulation code here (create processes, run the scheduler, and print results)

# avg_arrival_rate = 1 #this is lamda λ
sim_clock = SimulationClock(avg_arrival_rate, avg_service_time)
sim_clock.run(total_processes, scheduler, quantum)
