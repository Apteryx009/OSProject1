import random
from Event import Event
def FCFS(self):
    if not self.ready_queue:
        # If there are no processes in the ready_queue, advance time to the next process arrival.
        if len(self.allP) < self.total_processes:  # If there are still processes to be created
            next_arrival = random.expovariate(self.avg_arrival_rate)
            self.current_time += next_arrival  # Jump to next process arrival time
        else:
            self.current_time += 0.001  # Small default time increment if no processes are left
        return

    
    P = self.ready_queue[0]
    
    
    # If the current process hasn't arrived yet, advance time to its arrival
    if P.AT > self.current_time:
        self.totalIdle += abs(P.AT - self.current_time)
        
        self.current_time = P.AT  # Set the current_time to the Arrival Time of the process
        return

    # If the process has arrived, process it
    if P.BTLeft == P.BT:  # The process is just starting
        P.TimeOf1stService = self.current_time
        P.WT = P.TimeOf1stService - P.AT

    # Determine time quantum for the process 
    # It can be either the remaining burst time or the arrival of the next process
    if len(self.allP) < self.total_processes:
        next_process_AT = self.allP[len(self.ready_queue)].AT if len(self.allP) > len(self.ready_queue) else float("inf")
        time_quantum = min(P.BTLeft, next_process_AT - self.current_time)
    else:
        time_quantum = P.BTLeft

    P.BTLeft -= time_quantum
    #print(len(self.ready_queue))
    self.current_time += time_quantum

    # If the process has completed, remove it from the queue
    if P.BTLeft == 0:
        P.CT = self.current_time
        self.processed_processes += 1

      

        #print(len(self.ready_queue))
        
        self.ready_queue.remove(P)
        newEvent = Event(P, self.current_time, 2) 
        self.event_queue.append(newEvent)