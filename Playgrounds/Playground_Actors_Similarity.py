# Define the two phrases for comparison
from numpy import double


def determinate_full_name(token):
    """
    :param token: Token that is part of the extended name
    :return: full name as string
    """
    full_name_tokens = [token]  # TODO: should token (parameter) be added to the list?
    for subchild in token.children:
        if subchild.dep_ == "amod":
            full_name_tokens.extend(determinate_full_name(subchild))
        if subchild.dep_ == "compound":
            full_name_tokens.extend(determinate_full_name(subchild))

        if subchild.dep_ == "conj":  # TODO also work for or? Only for ex.5 NOUN AND NOUN
            full_name_tokens.extend(determinate_full_name(subchild))

        if subchild.dep_ == "cc":
            full_name_tokens.extend(determinate_full_name(subchild))

        if subchild.dep_ == "prep":
            full_name_tokens.extend(determinate_full_name(subchild))

        if subchild.dep_ == "pobj":
            full_name_tokens.extend(determinate_full_name(subchild))

    sorted_tokens = sorted(full_name_tokens, key=lambda token: token.i)
    return sorted_tokens


def compare_actors_similarity(Actor1: str, Actor2: str, nlp):
    import spacy
    criteria_similarity_score = 0.5
    criteria_similarity_ratio = 0.5
    similarity_score = compare_actors_with_similarity(Actor1, Actor2, nlp)
    similarity_ratio = compare_actors_with_token(Actor1, Actor2, nlp)
    result = similarity_score > criteria_similarity_score and similarity_ratio > criteria_similarity_ratio
    print("{:<60}{:<60}{:<20}{:<10}{:<10}".format(Actor1, Actor2, similarity_score, similarity_ratio, result.__str__()))
    return result


def compare_actors_with_similarity(Actor1: str, Actor2: str, nlp):
    doc1 = nlp(Actor1)
    doc2 = nlp(Actor2)
    similarity_score = round(doc1.similarity(doc2), 2)
    return similarity_score


# Define a function to compare actor names based on token lemma similarity
def compare_actors_with_token(Actor1: str, Actor2: str, nlp):
    # Process the actor names using spaCy
    doc1 = nlp(Actor1)
    doc2 = nlp(Actor2)

    # Filter out tokens where token.is_stop = True
    tokens1 = [token for token in doc1 if not token.is_stop]
    tokens2 = [token for token in doc2 if not token.is_stop]

    # Count the number of tokens for each actor
    num_tokens1 = len(tokens1)
    num_tokens2 = len(tokens2)

    # Initialize variables to count matching tokens
    matching_tokens = 0

    # Compare the tokens in the actor with fewer tokens with tokens in the other actor
    if num_tokens1 <= num_tokens2:
        for token1 in tokens1:
            for token2 in tokens2:
                if token1.lemma_ == token2.lemma_:
                    matching_tokens += 1
                    break  # Break the inner loop if a match is found
    else:
        for token2 in tokens2:
            for token1 in tokens1:
                if token2.lemma_ == token1.lemma_:
                    matching_tokens += 1
                    break  # Break the inner loop if a match is found

    # Calculate the average number of tokens between the two actors
    avg_tokens = (num_tokens1 + num_tokens2) / 2.0

    # Calculate the similarity ratio
    similarity_ratio = matching_tokens / avg_tokens if avg_tokens > 0 else 0.0

    # Return True if the similarity ratio is greater than 0.7, else False
    # print("Similarity similarity_ratio:", similarity_ratio)
    return similarity_ratio


def get_valid_actors_vh(container_list: [], nlp) -> list:
    """
    iterate the container list and get all the actors that are real actors
    check wheater the actor is already in the list, if not add it to the list
    Checking the similarity of the actors with the help of the function compare_actors_similarity

    Args:
        container_list: The container that contains the action.

    Returns:
        A list of actors that are real actors.

    """
    result = []
    for container in container_list:
        for process in container.processes:
            if process.actor is not None:
                process.actor.determinate_full_name1()
                if process.actor.is_real_actor:
                    temp_bool_add = True
                    for actor in result:
                        if compare_actors_similarity(process.actor.full_name, actor, nlp):
                            temp_bool_add = False
                            process.actor.full_name = actor
                            break
                    if temp_bool_add:
                        result.append(process.actor.full_name)
    return result


phrase1 = "sales person"
phrase2 = "sales department"

import spacy
nlp_similarity = spacy.load("en_core_web_lg")

# Example usage:

print(
    f"phrase1: {phrase1}, phrase2: {phrase2}, compare_actors_with_similarity(phrase1, phrase2): {compare_actors_with_similarity(phrase1, phrase2, nlp_similarity)}")
