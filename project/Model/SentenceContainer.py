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
