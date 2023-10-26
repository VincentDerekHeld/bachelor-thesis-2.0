import os
import openai

openai.api_key = "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"
openai.organization = "org-cGUe4rwtHg1jEuK4T5Ya9rU3"


# print(openai.Model.list())
# org-id = org-cGUe4rwtHg1jEuK4T5Ya9rU3


def LLMs1(textual_descrption: str):
    """
    This function is used to simplfy the language of a textual description by leveraging the GPT-3 LLMs.
    :param text_input: The textual description of a process.
    :return: The simplified textual description of a process.
    """
    list_of_promts: list = []
    promt0: str = """
    """
    # list_of_promts.append(promt0)
    promt1: str = """
    Try to return a text of short precise sentences, which contains only the process relevant information. 
    Decide carefully for each informationn if the information is relevant for the process. 
    -> The only information we are interested in are real process steps. 
    -> Filter the information that is not relevant for the process. Here are some examples that MUST be filtered:
         - Introductions
         - Explainations 
         - information on process instances are not relevant
    You handle every task sentence for sentence.
    You return the answers in full sentences without adding any extra information, interpretation, numberations or listings.
    TEXT:
    """
    list_of_promts.append(promt1)

    promt2: str = """
    2. Try to return a text of short precise sentences in active voice, which contain only the process relevant information:
    -> Modal verbs, that express the strength of an expression MUST be kept. Example modal verbs are: must, shall, should.
    -> ACTION, the ACTOR, the OBJECT and if there is a CONDITION.  
    -> If there is a condition try to structure the sentence like this „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“. 
    -> If two ACTIONs are based on the same CONDITION merge the sentences to a format like: „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“. 
    	Example: 
    	„If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours.“
    	„If the notification isn't made within 72 hours, the controller shall provide reasons for the delay.“
    	-> „If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours, else the controller shall provide reasons for the delay.“ 
    -> If process steps can be done in parallel start the sentence with „Meanwhile, ….“.

    TEXT:
    """
    list_of_promts.append(promt2)
    promt3: str = """
    3. Some sentences use implicit ACTIONS, also try to extract this information and make it explicit in the sentence format explained in Step 2.
    -> Example: „Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results.“ —> implies the ACTION „document the results“.
    4. Filter reasons for ACTIONs from the result.
    -> Example: „The organization must document information as evidence of the audit programme's implementation and the results.“ --> The correct output is: „The organization must document information of the audit programme's implementation and the results.“ , because „as evidence“ is an example.
    5. For the identification of the ACTOR, keep in mind, a actor can  for e.g. be a natural person, a organization, such as a company or a department, but sometimes also a device or a system can be an valide Actor. 
    6. The output has to contain full sentences and can not contain list items, such as bullet points.
    TEXT:

    """
    # list_of_promts.append(promt3)

    chat_response = textual_descrption
    messages = [{"role": "system",
                 "content": "You are a process analyst, that wants to simplyfiy the textual description of "
                            "a process or you want to describe a regulatory document as a simple process description, "
                            "that explain WHO has to take car of WHAT Actions. You return the answers in full sentences "
                            "without adding any extra information, interpretation, numberations or listings. "
                            "You handle every task sentence for sentence."}
                ]

    """
     messages.append({"assistant": "system",
                     "content": chat_response})  # store the response in the messages list to achieve a message history
    """

    for promt in list_of_promts:
        promt += chat_response
        content: str = promt
        print("Request: \n \t" + content)
        messages.append({"role": "user", "content": content})
        completion = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model="gpt-4",
            messages=messages
        )
        chat_response = completion.choices[0].message.content

        print("chat_response: \n \t", chat_response)

    return chat_response


def LLMs(text_input: str):
    """
    This function is used to simplfy the language of a textual description by leveraging the GPT-3 LLMs.
    :param text_input: The textual description of a process.
    :return: The simplified textual description of a process.
    """

    examples: list = []
    example1: str = """
    ### Input ###
    A small company manufactures customized bicycles. Whenever the sales department receives an order, a new process instance is created. A member of the sales department can then reject or accept the order for a customized bike. In the former case, the process instance is finished. In the latter case, the storehouse and the engineering department are informed. The storehouse immediately processes the part list of the order and checks the required quantity of each part. If the part is available in-house, it is reserved. If it is not available, it is back-ordered. This procedure is repeated for each item on the part list. In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle. Afterwards, the sales department ships the bicycle to the customer and finishes the process instance. 

    ### Output ###

    The sales department receives an order.
    A member of the sales department can then reject or accept the order for a customized bike. 
    In the sales department rejects, the process instance is finished, else the sales department inorms the storehouse and the engineering department.
    The storehouse immediately processes the part list of the order and checks the required quantity of each part. 
    If the part is available in-house, it is reserved, else it is back-ordered. 
    This procedure is repeated for each item on the part list. 
    In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. 
    If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle. 
    Afterwards, the sales department ships the bicycle to the customer. 
    """

    promt: str = """
    Follow carefully the instructions and solve the tasks sentence for sentence. Return a simple textual descitption, without adding any extra information, interpretation, numberations or listings.
    -> Example: do not add: „Following the provided instructions, here are the extracted process-relevant steps:“

    1. Decide if the information is relevant for the process. The only information we are interested in are real process steps.
        Examples:
         - Introductions are not relevant. 
         - Information on the start of the process / new process instances are not relevant.
         - Information on the end of the process / finished process instances are not relevant.
    	-> If the information is relevant for the process, use this information for the output.
    	-> If not, do not use this information for the output / filter it.

    2. Try to return a text of short precise sentences in active voice, which contain the process relevant information:
    -> Modal verbs, that express the strength of an expression MUST be kept. Example modal verbs are: must, shall, should.
    -> ACTION, the ACTOR, the OBJECT and if there is a CONDITION.  
    -> If there is a condition try to structure the sentence like this „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“. 
    -> If two ACTIONs are based on the same CONDITION merge the sentences to a format like: „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“. 
    	Example: 
    	„If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours.“
    	„If the notification isn't made within 72 hours, the controller shall provide reasons for the delay.“
    	-> „If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours, else the controller shall provide reasons for the delay.“ 
    -> If process steps can be done in parallel start the sentence with „Meanwhile, ….“.


    3. Some sentences use implicit ACTIONS, also try to extract this information and make it explicit in the sentence format explained in Step 2.
    -> Example: „Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results.“ —> implies the ACTION „document the results“.

    4. Filter reasons for ACTIONs from the result.
    -> Example: „The organization must document information as evidence of the audit programme's implementation and the results.“ --> The correct output is: „The organization must document information of the audit programme's implementation and the results.“ , because „as evidence“ is an example.

    5. Filter information that just adress that the process starts or is finished.
    -> Example: "The process instance is then finished."

    6. For the identification of the ACTOR, keep in mind, a actor can  for e.g. be a natural person, a organization, such as a company or a department, but sometimes also a device or a system can be an valide Actor. 

    7. The output has to contain full sentences and can not contain list items, such as bullet points.

    ############ Example: ############

    ### Input ###
    A small company manufactures customized bicycles. Whenever the sales department receives an order, a new process instance is created. A member of the sales department can then reject or accept the order for a customized bike. In the former case, the process instance is finished. In the latter case, the storehouse and the engineering department are informed. The storehouse immediately processes the part list of the order and checks the required quantity of each part. If the part is available in-house, it is reserved. If it is not available, it is back-ordered. This procedure is repeated for each item on the part list. In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle. Afterwards, the sales department ships the bicycle to the customer and finishes the process instance. 

    ### Output ###

    The sales department receives an order.
    A member of the sales department can then reject or accept the order for a customized bike. 
    In the sales department rejects, the process instance is finished, else the sales department inorms the storehouse and the engineering department.
    The storehouse immediately processes the part list of the order and checks the required quantity of each part. 
    If the part is available in-house, it is reserved, else it is back-ordered. 
    This procedure is repeated for each item on the part list. 
    In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. 
    If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle. 
    Afterwards, the sales department ships the bicycle to the customer. 

    ###### TEXT: ######

    """
    promt += text_input
    content: str = promt
    print("Request: \n \t" + content)
    messages = [{"role": "user", "content": content}]
    messages.append({"role": "system",
                     "content": "You are a process analyst, that wants to simplyfiy the textual description of a process or you want to describe a regulatory document as a simple process description, that explain WHO has to take car of WHAT Actions. You answer in full sentences, without any bullet points or listings."})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response: str = completion.choices[0].message.content
    messages.append({"assistant": "system",
                     content: chat_response})  # store the response in the messages list to achieve a message history
    print("chat_response: \n \t", chat_response)
    return chat_response


input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text1_GPT4.txt"
text_input = open(input_path, 'r').read().replace('\n', ' ')
# LLMs(text_input)
