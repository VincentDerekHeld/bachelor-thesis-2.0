class Activity:
    def __init__(self, process):
        self.id = None
        self.process = process
        self.next = None
        self.is_start_activity = False
        self.is_end_activity = False
