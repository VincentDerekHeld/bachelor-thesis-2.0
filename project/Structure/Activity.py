from Structure.Structure import Structure


class Activity(Structure):

    def __init__(self, process):
        super().__init__()
        self.process = process
        self.is_start_activity = False
        self.is_end_activity = False

    def __str__(self) -> str:
        activity = ""
        if self.process.actor is not None:
            activity += str(self.process.actor)
        if self.process.action is not None:
            if activity != "":
                activity += " "
            activity += str(self.process.action)
        return activity
