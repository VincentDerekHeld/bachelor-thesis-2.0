from typing import Optional


class Activity:
    ID_COUNTER = 0

    def __init__(self, process):
        self.id = Activity.ID_COUNTER
        Activity.ID_COUNTER += 1

        self.process = process
        self.next: Optional[Activity] = None
        self.is_start_activity = False
        self.is_end_activity = False
