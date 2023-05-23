from spacy.tokens import Doc, Span, Token
from Model.Process import Process


class SentenceContainer:
    def __init__(self, sentence: Span):
        self.sentence: Span = sentence
        self.processes: [Process] = []

    def __str__(self) -> str:
        return "Main sentence: \"" + self.sentence.text + "\""

    def add_process(self, process: Process):
        self.processes.append(process)

    def process_is_first(self, process: Process) -> bool:
        return process == self.processes[0]

    def has_if(self):
        return any(process.action.marker == "if" for process in self.processes)

    def has_else(self):
        return any(process.action.marker == "else" for process in self.processes)

    def remove_process(self, actor=None, action=None, sub_sentence=None):
        if actor is not None:
            for process in self.processes:
                if process.actor is not None and process.actor == actor:
                    self.processes.remove(process)

        if action is not None:
            for process in self.processes:
                if process.action is not None and process.action == action:
                    self.processes.remove(process)

        if sub_sentence is not None:
            for process in self.processes:
                if process.sub_sentence is not None and process.sub_sentence == sub_sentence:
                    self.processes.remove(process)