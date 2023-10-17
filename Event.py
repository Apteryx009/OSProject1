class Event:
        def __init__(self, Process, current_time, event_type):
            self.time = current_time
            self.type = event_type #1=arrival, 2=departure 3=swapping
            self.Process = Process