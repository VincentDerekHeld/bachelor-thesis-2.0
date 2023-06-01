from Model.ExtractedObject import ExtractedObject
from Model.Resource import Resource
from spacy.tokens import Token
from typing import Optional

from Utilities import str_utility, string_list_to_string


class Action(ExtractedObject):
    def __init__(self, verb):
        super().__init__(verb)
        self.verb_base_form: str = verb.lemma_
        self.object: Optional[Resource] = None
        self.conjunction: [Action] = []
        self.xcomp: Optional[Action] = None
        # "prt" stands for particle. -> It is a term used in dependency grammar to describe a relationship
        # between a verb and a particle in a phrasal verb.
        # She picked >up< the book.
        # They are looking >into< the problem.
        self.prt: Optional[Token] = None
        # Auxiliary verbs are verbs that are used together with a main verb to provide additional information
        # about the verb's tense, voice, or modality.
        # They >were< playing football.
        # She >had< already left when he arrived.
        self.aux: Optional[Token] = None
        self.advmod = []
        self.dative: Optional[Token] = None

        self.marker: Optional[str] = None
        self.pre_adv_mod: Optional[Token] = None
        self.prep: Optional[Token] = None

        self.negated: bool = False

        # self.link: Optional[Action] = None
        # todo: change to ENUM
        # self.link_type: Optional[str] = None
        # todo: what is this?
        # self.transient: bool = False

    def __str__(self) -> str:
        result = []
        if self.token is None:
            return ""

        str_utility(self.token, result)

        if self.prt is not None:
            str_utility(self.prt, result)
        if self.prep is not None:
            str_utility(self.prep, result)

        for mod in self.advmod:
            str_utility(mod, result)

        if self.negated:
            index = result.index(self.token)
            if index > -1:
                result.insert(index, "do not")

        if self.object is not None:
            str_utility(str(self.object), result, i=self.object.token.i)

        return string_list_to_string(result)
