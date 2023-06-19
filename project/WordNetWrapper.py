from Constant import PERSON_CORRECTOR_LIST, REAL_ACTOR_DETERMINERS, SUBJECT_PRONOUNS


# Define a function to get hypernyms
def get_hypernyms(token):
    hypernyms = []
    for synset in token._.wordnet.synsets():
        for hypernym in synset.hypernyms():
            hypernyms.extend([lemma.name() for lemma in hypernym.lemmas()])
    return set(hypernyms)


def can_be_person_or_system(full_noun: str, main_noun) -> bool:
    full_noun = full_noun.strip()
    if full_noun.lower() in PERSON_CORRECTOR_LIST:
        return True
    # elif main_noun.text.lower() in SUBJECT_PRONOUNS:
    #     return True
    synsets = main_noun._.wordnet.synsets()
    if len(synsets) == 0:
        return False
    elif can_be(synsets[0], []):
        return True
    else:
        return False

def can_be(synset, checked_words: list):
    if not synset.name() in checked_words:
        checked_words.append(synset.name())
        hypernyms = synset.hypernyms()
        if len(hypernyms) == 0:
            return False
        hypernym_name = hypernyms[0].lemma_names()[0]
        if hypernym_name in REAL_ACTOR_DETERMINERS:
            return True
        else:
            hypernyms = synset.hypernyms()
            if can_be(hypernyms[0], checked_words):
                return True
    else:
        return False


# todo: this function gives wrong result.
def is_meta_actor(main_noun, threshold=3):
    meta_terms = {'step', 'phase', 'stage', 'process', 'task', 'locomotion'}
    hyponym_count = 0

    for synset in main_noun._.wordnet.synsets():
        for hyponym in synset.hyponyms():
            if any(lemma.name() in meta_terms for lemma in hyponym.lemmas()):
                hyponym_count += 1
                if hyponym_count >= threshold:
                    return True
    return False
