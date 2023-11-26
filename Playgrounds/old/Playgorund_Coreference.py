import spacy

spacy.load("en_core_web_trf")

def get_valid_actors_vh1(container_list: [], nlp) -> list:
    """
    iterate the container list and get all the actors that are real actors
    check if the actor is already in the list, if not add it to the list
    Checking the similarity of the actors with the help of the function compare_actors_similarity

    Args:
        container_list: The container that contains the action.

    Returns:
        A list of actors that are real actors.

    """
    print("get_valid_actors_vh1")
    result = []
    for container in container_list:
        for process in container.processes:
            if process.actor is not None:
                process.actor.determinate_full_name_vh()
                print("Actor:", process.actor.full_name)
                if process.actor.is_real_actor:
                    temp_bool_add = True
                    for actor in result:
                        from Playgrounds.old.Playground_Actors_Similarity import compare_actors_similarity
                        if compare_actors_similarity(process.actor.full_name, actor, nlp):
                            temp_bool_add = False
                            process.actor.full_name = actor
                            break
                    if temp_bool_add:
                        result.append(process.actor.full_name)

    for actor_full_name in result:
        if actor_full_name.strip() in ["he", "he ", "she", "they", "it"]:
            result.remove(actor_full_name)
    return result
