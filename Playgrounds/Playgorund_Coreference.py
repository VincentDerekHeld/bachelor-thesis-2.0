import spacy

spacy.load("en_core_web_trf")

# Der gegebene Text
text5 = """The Evanstonian is an upscale independent hotel. 
When a guest calls room service at The Evanstonian, the room-service manager takes down the order. 
She then submits an order ticket to the kitchen to begin preparing the food. She also gives an order to the sommelier (i.e., the wine waiter) to fetch wine from the cellar and to prepare any other alcoholic beverages. 
Eighty percent of room-service orders include wine or some other alcoholic beverage. 
Finally, she assigns the order to the waiter. 
While the kitchen and the sommelier are doing their tasks, the waiter readies a cart (i.e., puts a tablecloth on the cart and gathers silverware). 
The waiter is also responsible for nonalcoholic drinks. Once the food, wine, and cart are ready, the waiter delivers it to the guestís room. 
After returning to the room-service station, the waiter debits the guestís account. The waiter may wait to do the billing if he has another order to prepare or deliver."""


def get_valid_actors_vh1(container_list: [], nlp) -> list:
    """
    iterate the container list and get all the actors that are real actors
    check wheater the actor is already in the list, if not add it to the list
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
                        from Playgrounds.Playground_Actors_Similarity import compare_actors_similarity
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
