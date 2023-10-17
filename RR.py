import random
from Event import Event

def RR(self, quantum):
    print("test")
    # Add newly arrived processes to the ready queue
    if not self.ready_queue:
        if len(self.allP) < self.total_processes:
            next_arrival = random.expovariate(self.avg_arrival_rate)
            self.current_time += next_arrival
        else:
            self.current_time += 0.001
        return

    # If no processes have arrived yet, then jump to the arrival of the next process
    if not self.ready_queue or self.ready_queue[0].AT > self.current_time:
        self.totalIdle += abs(self.ready_queue[0].AT - self.current_time) if self.ready_queue else 0
        self.current_time = self.ready_queue[0].AT if self.ready_queue else 0
        return

    # Round Robin scheduling
    self.ready_queue.sort(key=lambda p: p.AT)

    #this is for calc of avg proccesse in RQ
    time_difference = self.current_time - self.last_event_time
    self.integral_ready_queue += len(self.ready_queue) * time_difference
    self.last_event_time = self.current_time
    current_process = self.ready_queue.pop(0)

    

    # If the process is just starting, set its TimeOf1stService
    if current_process.TimeOf1stService is None:
        current_process.TimeOf1stService = self.current_time

    # Determine actual time slice for the process
    actual_quantum = min(quantum, current_process.BTLeft)
    current_process.BTLeft -= actual_quantum
    self.current_time += actual_quantum

    if current_process.BTLeft == 0:
        # Process has completed
        current_process.CT = self.current_time
        self.processed_processes += 1

        newEvent = Event(current_process, self.current_time, 2) 
        self.event_queue.append(newEvent)

    else:
        # Process was preempted
        newEvent = Event(current_process, self.current_time, 3) 
        self.event_queue.append(newEvent)
        
        self.ready_queue.append(current_process)

    # Calculate waiting times for other processes in the ready queue
    for process in self.ready_queue:
        if process.BTLeft != 0 and process.AT <= self.current_time:
            process.WT += actual_quantum
