from Model.ExtractedObject import ExtractedObject


class Actor(ExtractedObject):
    def __init__(self, token):
        super().__init__(token)
        # A “real”-Actor, as a person, an organization or a software system. -> [“person”, “social group”, “software system”]
        self.is_real_actor = True
        self.is_meta_actor = False
        # todo: I'm not sure the numbers should also be concluded in the class
        # self.__num_specifiers = []

    def __str__(self) -> str:
        return "Actor: \"" + self.token.text + "\""
