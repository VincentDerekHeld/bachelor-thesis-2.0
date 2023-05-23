from typing import Optional

from spacy.matcher.matcher import Matcher
from spacy.tokens import Doc, Span, Token

from Constant import SUBJECT_PRONOUNS, OBJECT_PRONOUNS
from Model.Actor import Actor
from Model.ExtractedObject import ExtractedObject
from Model.SentenceContainer import SentenceContainer
from Model.Action import Action


def find_dependency(dependencies: [str], sentence: Span = None, token: Token = None) -> [Token]:
    result = []
    if token is not None:
        for child in token.children:
            if child.dep_ in dependencies:
                result.append(child)

    elif sentence is not None:
        for token in sentence:
            for child in token.children:
                if child.dep_ in dependencies:
                    result.append(child)

    else:
        return None

    return result


def find_action(verb: Token, container: SentenceContainer) -> Optional[Action]:
    for process in container.processes:
        if process.action is not None and verb == process.action.token:
            return process.action
    return None


def find_actor(noun: Token, container: SentenceContainer) -> Optional[Actor]:
    for process in container.processes:
        if process.actor is not None and noun == process.actor.token:
            return process.actor
    return None


def find_process(container: SentenceContainer, action=None, actor=None, sub_sent=None):
    if action is not None:
        for process in container.processes:
            if process.action is not None and process.action == action:
                return process

    if actor is not None:
        for process in container.processes:
            if process.actor is not None and process.actor == actor:
                return process

    if sub_sent is not None:
        for process in container.processes:
            if process.sub_sentence is not None and process.sub_sentence == sub_sent:
                return process

def starts_with_any(phrase: str, indicators: [str]) -> bool:
    for indicator in indicators:
        if indicator.startswith(phrase):
            return True
    return False


def contains_indicator(rules, sentence: Span, nlp) -> bool:
    matcher = Matcher(nlp.vocab)
    for rule in rules:
        for k, v in rule.items():
            matcher.add(k, [v])

    matches = matcher(sentence)
    if len(matches) > 0:
        return True

    return False


def anaphora_resolver(obj: ExtractedObject):
    if not needs_resolve_reference(obj.token):
        return
    resolved_words = resolve_reference(obj.token)
    obj.resolved_token.extend(resolved_words)


def needs_resolve_reference(word: Token) -> bool:
    if word.text in SUBJECT_PRONOUNS or word.text in OBJECT_PRONOUNS:
        return True
    return False


def resolve_reference(to_be_resolved_word: Token) -> [Token]:
    if to_be_resolved_word is None:
        return []
    if to_be_resolved_word.doc._.coref_chains is None:
        return []

    resolved_word = to_be_resolved_word.doc._.coref_chains.resolve(to_be_resolved_word)
    if resolved_word is not None:
        return resolved_word
    else:
        return []


def belongs_to_other_process(root: Token, container: SentenceContainer):
    ancestor = next(root.ancestors)
    if ancestor is not None:
        if ancestor.pos_ == "AUX" or ancestor.pos_ == "VERB":
            action = find_action(ancestor, container)
            if action is not None:
                process = find_process(container, action=action)
                return container.processes.index(process)
    return None
