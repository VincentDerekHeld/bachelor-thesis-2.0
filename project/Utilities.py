from typing import Optional

from spacy.matcher.matcher import Matcher
from spacy.tokens import Span, Token
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
