import random
def SRTF(self):
    if not self.ready_queue:
        if len(self.allP) < self.total_processes:
            next_arrival = random.expovariate(self.avg_arrival_rate)
            self.current_time += next_arrival
        else:
            self.current_time += 0.001
        return

    self.ready_queue.sort(key=lambda p: p.BTLeft)
    
    # If the first process in the sorted queue hasn't arrived yet, 
    # we select the first process that has arrived
    index = 0
    while index < len(self.ready_queue) and self.ready_queue[index].AT > self.current_time:
        index += 1
    
    # If no processes have arrived yet, then jump to the arrival of the next process
    if index == len(self.ready_queue):
        self.current_time = self.ready_queue[0].AT
        return
    
    P = self.ready_queue.pop(index)
    print("working on ", P.process_id)

    if P.TimeOf1stService is None:
        P.TimeOf1stService = self.current_time
    elif P.LastPreempted is not None:  # Only add to waiting time if it's not the first service and was preempted earlier
        P.WT += (self.current_time - P.LastPreempted)

    if len(self.allP) < self.total_processes:
        next_process_AT = self.allP[len(self.ready_queue)].AT if len(self.allP) > len(self.ready_queue) else float("inf")
        time_quantum = min(P.BTLeft, next_process_AT - self.current_time)
    else:
        time_quantum = P.BTLeft

    P.BTLeft -= time_quantum
    self.current_time += time_quantum

    if P.BTLeft == 0:
        P.CT = self.current_time
        self.processed_processes += 1
    else:
        # If the process hasn't completed, update LastPreempted and put it back in the ready_queue
        P.LastPreempted = self.current_time
        self.ready_queue.append(P)
