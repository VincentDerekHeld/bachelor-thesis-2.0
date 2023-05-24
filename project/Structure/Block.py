from enum import Enum

from Model.SentenceContainer import SentenceContainer


class ConditionType(Enum):
    IF = "if"
    ELSE = "else"


class ConditionBlock:
    def __init__(self):
        self.branches = []
        self.next = None

    def add(self, container: SentenceContainer):
        for process in container.processes:
            if process.action is None:
                continue
            if process.action.marker == "if":
                branch = {"type": ConditionType.IF, "condition": process, "actions": []}
                self.branches.append(branch)
            if process.action.marker == "else":
                branch = {"type": ConditionType.ELSE, "condition": None, "actions": [process]}
                self.branches.append(branch)
