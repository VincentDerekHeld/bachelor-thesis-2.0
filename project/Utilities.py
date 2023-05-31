from typing import Optional

from spacy.matcher.matcher import Matcher
from spacy.tokens import Doc, Span, Token

from Constant import SUBJECT_PRONOUNS, OBJECT_PRONOUNS
from Model.Actor import Actor
from Model.ExtractedObject import ExtractedObject
from Model.Process import Process
from Model.SentenceContainer import SentenceContainer
from Model.Action import Action


def find_dependency(dependencies: [str], sentence: Span = None, token: Token = None) -> [Token]:
    """
    find tokens that has the corresponding dependency in the specified dependencies list

    Args:
        dependencies: list of dependencies that we want to find
        sentence: do we want to find dependency in a sentence?
        token: or do we just to find dependency in the children of a token?

    Returns:
        list of tokens

    """
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
    """
    given a verb in form of Token, find the corresponding action in the container

    Args:
        verb: the verb used to find the action
        container: the container that contains the action

    Returns:
        the action that corresponds to the verb

    """
    for process in container.processes:
        if process.action is not None and verb == process.action.token:
            return process.action
    return None


def find_actor(noun: Token, container: SentenceContainer) -> Optional[Actor]:
    """
    given a noun in form of Token, find the corresponding actor in the container

    Args:
        noun: the noun used to find the actor
        container: the container that contains the actor

    Returns:
        the actor that corresponds to the noun

    """
    for process in container.processes:
        if process.actor is not None and noun == process.actor.token:
            return process.actor
    return None


def find_process(container: SentenceContainer, action=None, actor=None, sub_sent=None) -> Optional[Process]:
    """
    find the process that has the given action, actor, or sub_sentence

    Args:
        container: the container that contains the process
        action: action in the process
        actor: actor in the process
        sub_sent: sub_sentence in the process

    Returns:
        the founded process

    """
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

    return None


def contains_indicator(rules, sentence: Span, nlp) -> bool:
    """
    check if the sentence contains indicator specified in the given rules (spacy matchers)

    Args:
        rules: spacy matcher rules used to find the indicator
        sentence: the sentence to be checked
        nlp: spacy nlp language model

    Returns:
        True if the sentence contains the indicator, False otherwise

    """
    matcher = Matcher(nlp.vocab)
    for rule in rules:
        for k, v in rule.items():
            matcher.add(k, [v])

    matches = matcher(sentence)
    if len(matches) > 0:
        return True

    return False


def anaphora_resolver(obj: ExtractedObject):
    """
    resolve the anaphora in the given object

    Args:
        obj: the actor or resource to be resolved

    """
    if not needs_resolve_reference(obj.token):
        return
    resolved_words = resolve_reference(obj.token)
    obj.resolved_token.extend(resolved_words)


def needs_resolve_reference(word: Token) -> bool:
    """
    check if the given word needs to be resolved

    Args:
        word: the word to be checked

    Returns:
        True if the word needs to be resolved, False otherwise

    """
    if word.text in SUBJECT_PRONOUNS or word.text in OBJECT_PRONOUNS:
        return True
    return False


def resolve_reference(to_be_resolved_word: Token) -> [Token]:
    """
    resolve the given word

    Args:
        to_be_resolved_word: the word to be resolved

    Returns:
        the resolved word in form of list
    """
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
    """
    check if the given root token belongs to other action

    Args:
        root: the root token to be checked
        container: the container that contains the whole processes

    Returns:
        the process contains the given root token, None otherwise

    """
    if len(list(root.ancestors)) > 0:
        ancestor = next(root.ancestors)
    else:
        ancestor = None
    if ancestor is not None:
        if ancestor.pos_ == "AUX" or ancestor.pos_ == "VERB":
            action = find_action(ancestor, container)
            if action is not None:
                process = find_process(container, action=action)
                return container.processes.index(process)
    return None
