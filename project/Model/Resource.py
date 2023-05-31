from Model.ExtractedObject import ExtractedObject
from spacy.tokens import Token


class Resource(ExtractedObject):
    def __init__(self, token):
        super().__init__(token)
        self.resolved_token: [Token] = []

    def __str__(self) -> str:
        resource = ""
        if self.token is None:
            return resource
        else:
            if len(self.resolved_token) > 0:
                for r in self.resolved_token:
                    resource += r.text
                    if self.resolved_token.index(r) != len(self.resolved_token) - 1:
                        resource += ", "
            else:
                resource = self.token.text

            if self.determiner is not None:
                resource = self.determiner.text + " " + resource

            return resource
