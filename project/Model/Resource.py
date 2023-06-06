from Model.ExtractedObject import ExtractedObject
from spacy.tokens import Token
from Utilities import str_utility, string_list_to_string


class Resource(ExtractedObject):
    def __init__(self, token):
        super().__init__(token)
        self.resolved_token: [Token] = []

    def __str__(self) -> str:
        resource = []
        if self.token is None:
            return ""
        else:
            if len(self.resolved_token) > 0:
                for r in self.resolved_token:
                    str_utility(r, resource)
            else:
                str_utility(self.token, resource)

            if self.determiner is not None:
                str_utility(self.determiner, resource)
            for comp in self.compound:
                str_utility(comp, resource)
            for spec in self.specifiers:
                if spec.SpecifierType.value == "amod":
                    str_utility(spec.token, resource)

            return string_list_to_string(resource)
