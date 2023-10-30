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
    list_of_promts.append(promt3)

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
    promt = open("/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Playgrounds/LLMs_Prompts", 'r').read()
    promt += text_input
    content: str = promt
    print("Request: \n \t" + content)
    messages = [{"role": "user", "content": content}]
    messages.append({"role": "system",
                     "content": "You are a process analyst, that wants to simplyfiy the textual description of a process or you want to describe a regulatory document as a simple process description, that explain WHO has to take care of WHAT Actions. You answer in full sentences, without any bullet points or listings."})
    completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4-32k",
        # model="gpt-4",
        messages=messages
    )
    chat_response: str = completion.choices[0].message.content
    messages.append({"assistant": "system",
                     content: chat_response})  # store the response in the messages list to achieve a message history
    print("chat_response: \n \t", chat_response)
    return chat_response


def LLMs_da_vinci(text_input: str):
    """ This function is used to simplfy the language of a textual description by leveraging the GPT-3 LLMs.
    :param text_input: The textual description of a process.
    :return: The simplified textual description of a process. """
    # prompt = input("Input: ")
    promt = open("/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Playgrounds/LLMs_Prompts", 'r').read()
    promt += text_input
    content: str = promt
    print("Request: \n \t" + content)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=content + "---\n",
        # prompt=f"Assistant acts like a super funny mexican guy. Assistant speaks english. He mimics all of those classic mexican accents though. He's very nice and amusing to talk to.\n\nHuman: {prompt}\nAssistant:",
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["---"],
        stream=False
    )

    chat_response: str = response.choices[0].text
    print("chat_response: \n \t", chat_response)