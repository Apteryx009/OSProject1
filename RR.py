import random

def RR(self, processes, quantum):
        #print(self.current_time)
        # Add newly arrived processes to the ready queue
        for process in processes:
            if process.AT <= self.current_time and process not in self.ready_queue and process.CT is None:
                self.ready_queue.append(process)

        if not self.ready_queue:
            # No processes in the ready queue, advance time
            self.current_time += 0.00000001
        
        
        else:
            #self.ready_queue.sort(key=lambda p: p.AT)
            # Round Robin scheduling
            current_process = self.ready_queue.pop(0)
            
            # If the process is just starting, set its TimeOf1stService
            if current_process.process_id != 1:
                if current_process.TimeOf1stService is None:
                    current_process.TimeOf1stService = self.current_time
            else:
                current_process.TimeOf1stService = current_process.AT
            
           

            # Determine actual time slice for the process
            actual_quantum = min(quantum, current_process.BTLeft)
            current_process.BTLeft -= actual_quantum
            self.current_time += current_process.AT
            self.current_time += actual_quantum

            #print(self.current_time)
            if current_process.BTLeft == 0:
                # Process has completed
                #print("Process ", current_process.process_id, " has completed")
                current_process.CT = self.current_time
                self.processed_processes += 1
            else:
                # Process was preempted
                self.ready_queue.append(current_process)

            # Calculate waiting times for other processes in the ready queue
            for process in self.ready_queue:
                if process.BTLeft != 0:
                    process.WT += actual_quantum