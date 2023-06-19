from enum import Enum

from Model.SentenceContainer import SentenceContainer
from Structure.Activity import Activity
from Structure.Structure import Structure, StructureType


class ConditionType(Enum):
    IF = "if"
    ELSE = "else"


class ConditionBlock(Structure):
    def __init__(self):
        super().__init__()
        self.type = StructureType.CONDITION
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

    def merge_branches(self, incoming: "ConditionBlock"):
        for branch in incoming.branches:
            self.branches.append(branch)

    def create_dummy_branch(self):
        branch = {"type": ConditionType.ELSE, "condition": None, "actions": []}
        self.branches.append(branch)

    def is_complete(self):
        if len(self.branches) == 1:
            return False
        else:
            return True

    def __str__(self) -> str:
        string = ""
        string += "-----BEGIN_IF-----\n"
        for branch in self.branches:
            if branch["type"] == ConditionType.IF:
                string += "if: " + str(branch["condition"]) + ":\n"
            elif branch["type"] == ConditionType.ELSE:
                string += "else:\n"
            for action in branch["actions"]:
                if self.branches.index(branch) == len(self.branches) - 1 and branch["actions"].index(action) == len(
                        branch["actions"]) - 1:
                    string += "\t" + str(action)
                else:
                    string += "\t" + str(action) + "\n"
        string += "\n-----END_IF-----"
        return string


class AndBlock(Structure):
    def __init__(self):
        super().__init__()
        self.type = StructureType.PARALLEL
        self.branches = []

    def add_branch(self, container: SentenceContainer):
        branch = []

        for process in container.processes:
            if process.action is None:
                continue
            else:
                branch.append(Activity(process))

        self.branches.append(branch)

    def __str__(self) -> str:
        string = ""
        string += "-----BEGIN_AND-----\n"
        for branch in self.branches:
            string += str(self.branches.index(branch) + 1) + ":\n"
            for action in branch:
                if self.branches.index(branch) == len(self.branches) - 1 and branch.index(action) == len(
                        branch) - 1:
                    string += "\t" + str(action)
                else:
                    string += "\t" + str(action) + "\n"
        string += "\n-----END_AND-----"
        return string
