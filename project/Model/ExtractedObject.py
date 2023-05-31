from typing import Optional
from spacy.tokens import Token
from Model.Specifier import Specifier
from Model.SpecifierType import SpecifierType


class ExtractedObject:

    def __init__(self, token):
        self.token: Token = token
        # Some examples of determiners in English include "a", "an", "the", "this", "that", "these", "those",
        # "my", "your", "his", "her", "its", "our", and "their".
        self.determiner: Optional[Token] = None
        self.compound: [Token] = []

        self.modifiers: [Specifier] = []

    def add_compound(self, compound):
        self.compound.extend(compound)

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    def get_specifiers(self, specifier_type: [SpecifierType] = None) -> [Specifier]:
        if specifier_type is None:
            return self.modifiers
        else:
            result = []
            for m in self.modifiers:
                if m.SpecifierType.value in specifier_type:
                    result.append(m)
            return result
