from spacy.tokens import Token
from project.Model import SpecifierType


class Specifier:
    def __init__(self, token, specifier_type, name):
        self.SpecifierType: SpecifierType = specifier_type
        self.token: Token = token
        self.name = name.lower()