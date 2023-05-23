from Model.ExtractedObject import ExtractedObject
from spacy.tokens import Token


class Resource(ExtractedObject):
    def __init__(self, token):
        super().__init__(token)
        self.resolved_token: [Token] = []

    def __str__(self) -> str:
        return "Resource: \"" + self.token.text + "\""
