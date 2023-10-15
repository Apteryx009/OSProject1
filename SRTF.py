import random

def SRTF(self):
    if not self.ready_queue:
        if len(self.allP) < self.total_processes:
            next_arrival = random.expovariate(self.avg_arrival_rate)
            self.current_time += next_arrival
        else:
            self.current_time += 0.001
        return

    # Only consider processes that have already arrived
    arrived_processes = [p for p in self.ready_queue if p.AT <= self.current_time]
    
    # If no processes have arrived yet, then jump to the arrival of the next process
    if not arrived_processes:
        self.totalIdle += abs(self.ready_queue[0].AT - self.current_time)
        self.current_time = self.ready_queue[0].AT
        return

    # Sort by BTLeft and select the process with the lowest processing time left
    P = min(arrived_processes, key=lambda x: x.BTLeft)

    #this is for calc of avg proccesse in RQ
    time_difference = self.current_time - self.last_event_time
    self.integral_ready_queue += len(self.ready_queue) * time_difference
    self.last_event_time = self.current_time
    
    self.ready_queue.remove(P)
    
    if P.TimeOf1stService is None:
        P.TimeOf1stService = self.current_time
    
    # Calculate the time quantum
    next_arrival_time = min([proc.AT for proc in self.ready_queue if proc.AT > self.current_time], default=float('inf'))
    time_quantum = min(P.BTLeft, next_arrival_time - self.current_time)
    
    # Execute the process for the duration of time_quantum
    P.BTLeft -= time_quantum
    self.current_time += time_quantum

    if P.BTLeft == 0:
        P.CT = self.current_time
        self.processed_processes += 1
    else:
        P.LastPreempted = self.current_time
        self.ready_queue.append(P)

    # Calculate waiting times for other processes in the ready queue
    for process in self.ready_queue:
        if process.BTLeft != 0:
            process.WT += time_quantum
