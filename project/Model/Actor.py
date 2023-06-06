from Model.ExtractedObject import ExtractedObject
from spacy.tokens import Token
from Utilities import str_utility, string_list_to_string


class Actor(ExtractedObject):
    def __init__(self, token):
        super().__init__(token)
        self.resolved_token: [Token] = []
        # A “real”-Actor, as a person, an organization or a software system. -> [“person”, “social group”, “software system”]
        self.is_real_actor = True
        self.is_meta_actor = False
        # todo: I'm not sure the numbers should also be concluded in the class
        # self.__num_specifiers = []

    def __str__(self) -> str:
        actor = []
        if self.token is None:
            return ""
        else:
            if len(self.resolved_token) > 0:
                for a in self.resolved_token:
                    str_utility(a, actor)
            else:
                str_utility(self.token, actor)

            if self.determiner is not None:
                str_utility(self.determiner, actor)
            for comp in self.compound:
                str_utility(comp, actor)
            for spec in self.specifiers:
                if spec.SpecifierType.value == "amod":
                    str_utility(spec.token, actor)

            return string_list_to_string(actor)
