import random
def HRRN(self):
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

    # Calculate Response Ratio for each process and select the one with the highest RR
    for process in arrived_processes:
        if process.TimeOf1stService is None:
            process.WT = self.current_time - process.AT
        else:
            process.WT += self.current_time - process.LastPreempted
        
        process.RR = (process.WT + process.BT) / process.BT
        print("RR for ", process.process_id, " is ", process.RR, " at time ", self.current_time)

    # Sort by RR and select the process with the highest RR
    P = max(arrived_processes, key=lambda x: x.RR)
    #print("Selected to work on ", P.process_id)

    
    #this is for calc of avg proccesse in RQ
    time_difference = self.current_time - self.last_event_time
    self.integral_ready_queue += len(self.ready_queue) * time_difference
    self.last_event_time = self.current_time
    self.ready_queue.remove(P)

    if P.TimeOf1stService is None:
        P.TimeOf1stService = self.current_time

    # Since HRRN is non-preemptive, the entire burst time of the process is executed
    self.current_time += P.BT
    P.CT = self.current_time
    self.processed_processes += 1
