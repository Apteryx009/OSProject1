import random

def RR(self, processes, quantum):
    # Add newly arrived processes to the ready queue
    for process in processes:
        if process.AT <= self.current_time and process not in self.ready_queue and process.CT is None:
            self.ready_queue.append(process)

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
    else:
        # Process was preempted
        self.ready_queue.append(current_process)

    # Calculate waiting times for other processes in the ready queue
    for process in self.ready_queue:
        if process.BTLeft != 0 and process.AT <= self.current_time:
            process.WT += actual_quantum
