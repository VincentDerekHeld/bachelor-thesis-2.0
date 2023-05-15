from Model.ExtractedObject import ExtractedObject


class Resource(ExtractedObject):
    def __init__(self, token):
        super().__init__(token)

    def __str__(self) -> str:
        return "Resource: \"" + self.token.text + "\""
