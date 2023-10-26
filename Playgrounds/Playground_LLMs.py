import openai

openai.api_key = "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"
openai.organization = "org-cGUe4rwtHg1jEuK4T5Ya9rU3"


def LLMs_Steps(input_prompt: str, text_input: str) -> str:
    input_prompt += text_input
    print("Request: \n \t" + input_prompt)
    messages = [{"role": "user", "content": input_prompt}]
    messages.append({"role": "system",
                     "content": "You are a process analyst, that wants to simplyfiy the textual description of a process or you want to describe a regulatory document as a simple process description, that explain WHO has to take care of WHAT Actions. You answer in full sentences, without any bullet points or listings."})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response: str = completion.choices[0].message.content
    messages.append({"assistant": "system",
                     input_prompt: chat_response})  # store the response in the messages list to achieve a message history
    #print("chat_response: \n \t", chat_response)
    return chat_response


def run_multiple_prompts(input_text: str):
    promt1 = ("""
           Follow carefully the instructions and solve the following problem information for information. Return a simple textual descritption, without adding any extra information, interpretation, numberations or listings.
           -> Example: do not add: „Following the provided instructions, here are the extracted process-relevant steps:“
           Decide if the information is relevant for the process. The only information we are interested in are real process steps.
               Examples:
                - Introductions are not relevant.
                - Information on the start of the process / new process instances are not relevant.
                - Information on the end of the process / finished process instances are not relevant.
                -  information that just adress that the process starts or is finished.
                    -> Example: "The process instance is then finished."
           	-> If the information is relevant for the process, use this information for the output.
           	-> If not, do not use this information for the output / filter it. \n
           	###### TEXT ###### \n
           	""")
    input_text = LLMs_Steps(promt1, input_text)
    print("Prompt 1 Answer: \n" + input_text)

    promt2 = ("""
     Follow carefully the instructions and solve the following problem information for information. Return a simple textual descritption, without adding any extra information, interpretation, numberations or listings.
           -> Example: do not add: „Following the provided instructions, here are the extracted process-relevant steps:“
    2. Try to return a text of short precise sentences in active voice, which contain the process relevant information:
    -> Modal verbs, that express the strength of an expression MUST be kept.
        Example modal verbs are: must, shall, should.
    -> ACTION, the ACTOR, the OBJECT and "if", if there is a CONDITION.
     -> "When" can be replaced with "If"
     -> "Otherwise" can be replaced with "Else"
     -> For the identification of the ACTOR, keep in mind, a actor can  for e.g. be a natural person, a organization, such as a company or a department, but sometimes also a place, a device or a system can be an valide Actor.
            -> Example: The "Kitchen" represents the "kitchen staff", and so the "Kitchen" is an actor.
    -> If there is a condition try to structure the sentence like this „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“.
    -> If two ACTIONs are based on the same CONDITION merge the sentences to a format like: „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“.
    	Example 1:
    	    „If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours.“
    	    „If the notification isn't made within 72 hours, the controller shall provide reasons for the delay.“
    	    -> „If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours, else the controller shall provide reasons for the delay.“ 
        Example 2:
            „The room-service manager at The Evanstonian takes down the order when a guest calls room service.“
            -> If a guest calls room service, the room-service manager at takes down the order.
                Reasons:
                - „The Evanstonian“ is the company and is not relevant for the activity. It represents meta information.
    -> If process steps can be done in parallel start the sentence with „Meanwhile, ….“.
        Example:
        "The ongoing repair consists of two activities, which are executed, in an arbitrary order. The first activity is to check and repair the hardware, whereas the second activity checks and configures the software."
        -> "The Computer Repair Service (CRS) checks and repairs the hardware. In the meanwhile, the Computer Repair Service (CRS) checks and configures the software."
    -> Try to keep the words of the original text, if possible.
    """)
    input_text = LLMs_Steps(promt2, input_text)
    print("Prompt 2 Answer: \n" + input_text)

    promt3 = """
     Follow carefully the instructions and solve the following problem information for information. Return a simple textual descritption, without adding any extra information, interpretation, numberations or listings.
           -> Example: do not add: „Following the provided instructions, here are the extracted process-relevant steps:“
        
        Some sentences use implicit ACTIONS, also try to extract this information and make it explicit in the sentence format explained in Step 2.
        Example 1:
            „Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results.“
            -> implies the ACTION „document the results“.
        Example 2:
            "The Room Service Manager then submits an order ticket to the kitchen to begin preparing the food."
            -> „The Room Service Manager submits an order ticket to the kitchen. The kitchen prepares the food.“
            Make sure to keep the order of the sentences and to explicitly name the ACTOR and the ACTION.
    """
    input_text = LLMs_Steps(promt3, input_text)
    print("Prompt 3 Answer: \n" + input_text)

    promt4 = """
    Follow carefully the instructions and solve the following problem information for information. Return a simple textual descritption, without adding any extra information, interpretation, numberations or listings.
           -> Example: do not add: „Following the provided instructions, here are the extracted process-relevant steps:“
        Resolve references:
        "she, he, it" refer to an actor. Try to replace the reference with the name of the actor.
        "this, that" refer to an object. Try to replace the reference with the name of the object.
        "these, those" refer to multiple objects. Try to replace the reference with the name of the objects.
    """
    input_text = LLMs_Steps(promt4, input_text)
    print("Prompt 4 Answer - Reference Resolution \n" + input_text)


    promt5 = """
    5. Filter reasons for ACTIONs from the result.
    -> Example: „The organization must document information as evidence of the audit programme's implementation and the results.“ --> The correct output is: „The organization must document information of the audit programme's implementation and the results.“ , because „as evidence“ is an example.
    """
    input_text = LLMs_Steps(promt5, input_text)
    print("Prompt 5 Answer: \n" + input_text)

def run__setof_texts():
    itaration = 1
    while itaration < 24:
        if itaration in [5]:
            input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
            text_input = open(input_path, 'r').read().replace('\n', ' ')
            run_multiple_prompts(text_input)
        itaration += 1


run__setof_texts()
