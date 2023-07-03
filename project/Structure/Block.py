from enum import Enum

from Model.Process import Process
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
                branch = {"type": ConditionType.IF, "condition": [], "actions": []}
                if process.action.subclause is None:
                    branch["condition"].append(Activity(process))
                else:
                    branch["condition"].append(Activity(process.action.subclause))
                self.branches.append(branch)
                continue
            elif process.action.marker == "else":
                branch = {"type": ConditionType.ELSE, "condition": [], "actions": []}
                branch["actions"].append(Activity(process))
                self.branches.append(branch)
                continue

            if process.action.token.dep_ == "conj":
                father = next(process.action.token.ancestors)
                for condition_activity in self.branches[-1]["condition"]:
                    if condition_activity.process.action.token == father:
                        self.branches[-1]["condition"].append(Activity(process))
                        break
            elif len(self.branches) > 0:
                self.branches[-1]["actions"].append(Activity(process))

    def can_be_added(self, container: SentenceContainer) -> bool:
        for process in container.processes:
            if process.action is None:
                continue

            if process.action.marker == "else":
                return True
            elif process.action.marker == "if":
                for branch in self.branches:
                    for condition in branch["condition"]:
                        if condition.process.action.active:
                            reference_actor = condition.process.actor
                        else:
                            reference_actor = condition.process.action.object

                        if process.action.active:
                            compare_actor = process.actor
                        else:
                            compare_actor = process.action.object

                        if compare_actor is not None:
                            if reference_actor.token.text.lower() == compare_actor.token.text.lower():
                                return True
                return False

    def merge_branches(self, incoming: "ConditionBlock"):
        for branch in incoming.branches:
            self.branches.append(branch)

    def create_dummy_branch(self):
        branch = {"type": ConditionType.ELSE, "condition": [], "actions": []}
        self.branches.append(branch)

    def is_complete(self):
        if len(self.branches) == 1:
            return False
        else:
            return True

    def is_simple(self):
        if len(self.branches) == 2:
            if self.branches[0]["type"] == ConditionType.IF and self.branches[1]["type"] == ConditionType.ELSE:
                return True

        return False

    def __str__(self) -> str:
        string = ""
        string += "-----BEGIN_IF-----\n"
        for branch in self.branches:
            if branch["type"] == ConditionType.IF:
                string += "if: "
                for condition in branch["condition"]:
                    string += str(condition)
                    if branch["condition"].index(condition) != len(branch["condition"]) - 1:
                        string += ", "
                    else:
                        string += "\n"
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
