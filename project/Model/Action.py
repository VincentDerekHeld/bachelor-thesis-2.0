from Model.ExtractedObject import ExtractedObject
from Model.Resource import Resource
from spacy.tokens import Token
from typing import Optional


class Action(ExtractedObject):
    # todo: implement the inheritance of the super-class the specifiers before all!
    def __init__(self, verb):
        super().__init__(verb)
        self.verb_base_form: str = verb.lemma_
        self.object: Optional[Resource] = None
        # todo: implement the conjunction part -> see sentence "the CRS checks the defect and hands out a repair cost calculation"
        self.conjunction: Optional[Action] = None
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
        # todo: Check why the advmod must be set here?
        # "advmod" stands for adverbial modifier. -> It provides additional information about the action or state
        # described by the modified word, such as manner, degree, frequency, or time.
        # He runs >quickly<.
        # They >often< visit the park.
        # "acomp" stands for adjectival complement. -> It serves as the complement of a linking verb
        # (like "be", "seem", "become", "feel", etc.) and provides more information about the subject of the sentence.
        # The cake tastes >delicious<.
        # He became >tired< after the long journey.
        self.mod: Optional[Token] = None
        self.dative: Optional[Token] = None

        self.marker: Optional[str] = None
        self.marker_from_PP: bool = False
        self.pre_adv_mod: Optional[Token] = None
        self.prep: Optional[Token] = None

        self.negated: bool = False

        self.link: Optional[Action] = None
        # todo: change to ENUM
        # self.link_type: Optional[str] = None
        # todo: what is this?
        # self.transient: bool = False

    def __str__(self) -> str:
        return "Action: \"" + self.token.text + "\" " + self.object.__str__()
