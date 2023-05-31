from enum import Enum

from Model.SentenceContainer import SentenceContainer
from Structure.Activity import Activity
from Structure.Structure import Structure


class ConditionType(Enum):
    IF = "if"
    ELSE = "else"


class ConditionBlock(Structure):
    def __init__(self):
        super().__init__()
        self.branches = []

    def add_branch(self, container: SentenceContainer):
        for process in container.processes:
            if process.action is None:
                continue

            if process.action.marker == "if":
                branch = {"type": ConditionType.IF, "condition": Activity(process), "actions": []}
                self.branches.append(branch)
                continue
            elif process.action.marker == "else":
                branch = {"type": ConditionType.ELSE, "condition": None, "actions": []}
                branch["actions"].append(Activity(process))
                self.branches.append(branch)
                continue

            if len(self.branches) > 0:
                self.branches[-1]["actions"].append(Activity(process))

    def __str__(self) -> str:
        string = ""
        for branch in self.branches:
            if branch["type"] == ConditionType.IF:
                string += "if: " + str(branch["condition"]) + ":\n"
            elif branch["type"] == ConditionType.ELSE:
                string += "else:\n"
            for action in branch["actions"]:
                string += "\t" + str(action) + "\n"
        return string


class AndBlock:
    def __init__(self):
        self.branches = []
        self.next = None
