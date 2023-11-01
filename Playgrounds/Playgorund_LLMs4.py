import os
import openai
import spacy


def preprocess_text_with_LLM(text_input):
    # generate a response of an llm (open-ai) given a prompt
    debug_mode = True
    os.environ["OPENAI_API_KEY"] = "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"
    openai.api_key = "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"
    openai.organization = "org-cGUe4rwtHg1jEuK4T5Ya9rU3"
    intro = """You are a system analyst, that strictly and carefully follows the instructions. 
           You return only the current sentence as an full sentences without adding any extra information, interpretation, explanation, numberations or listings. 
           Make sure that the previously given instructions are still followed.
           Keep as much words from the original text as possible.
           You handle every task sentence for sentence. \n"""

    prompts = []
    inital_prompt = ("""
     ### Instuction: #### \n
     First, you will see the full text and read it carefully. Afterwards you will see parts of the text and you will follow the instructions.
     On this message you return an empty message as answer.
     ### Full Text ### \n
     
    """)
    # Relevance of Sentence
    prompts.append("""
        ### Instuction: #### \n
        Filter information from the text, that is not relevant for the process. The only information we are interested in are real process steps.
        ## Examples: ##
            - Introductions that decribe the goal of the process or what the company produces are not relevant.
                Example: "to ensure valid results. "
                    -> "The organization shall determine the methods for monitoring, measurement, analysis and evaluation, to ensure valid results" -> "The organization shall determine the methods for monitoring, measurement, analysis and evaluation"
                Example: "as evidence of the implementation of the audit programme(s)"
                    -> "Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results." -> "... shall document the results."
            -  information that just adress that the process starts or is finished.
                -> Example: "The process instance is then finished."
            - Information that clarifies that something is not universally applicaple
                -> Example: "as applicable"
                    "The organization shall determine the methods for monitoring, measurement, analysis and evaluation, as applicable," -> The organization shall determine the methods for monitoring, measurement, analysis and evaluation"
            - Examples are not relevant
            - Includign parts
                -> Example: "The organization shall determine what needs to be monitored and measured, including information security processes and controls" -> "The organization shall determine what needs to be monitored and measured"
        ###### TEXT ###### \n""")

    # Active Voice
    prompts.append(
        """
        Transform every sentence into an active voice sentence. 
        """
    )

    # Restructuring of sentences
    prompts.append("""
    Restructure every sentence to achieve the following format:
        "[ACTOR] [MODAL VERB] [VERB in active] [OBJECT]."
    ->  Actors are the subject of a sentence, or the person or thing that performs the action of the verb
        For the identification of the ACTOR, keep in mind, a actor can  for e.g. be a natural person, a organization, such as a company or a department, but sometimes also a place, a device or a system can be an valide Actor.
                -> Example: The "Kitchen" represents the "kitchen staff", and so the "Kitchen" is an actor.
        Make sure not to use Objects as Actors:
            Example: "select auditors"
                -> "auditors" are the object, not the actor


    Modal verbs have to stay with the original format  in the sentence.
    -> Modal verbs, are verbs that express the strength of an expression. 
        Example modal verbs are: "must", "shall", "should", "can".
         "Example 1: "The organization shall determine..." -> "The organization shall determine..." 
            Reason: "shall" must stay in the same format, as it is an "modal verb"

    If there is an condition, strucutre the sentence like this:
        „If [CONDITION], [ACTOR and ACTION], ELSE [other ACTION, if possible]“.
            Example 1:
        	    „If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours.“
        	    „If the notification isn't made within 72 hours, the controller shall provide reasons for the delay.“
        	    -> „If the controller becomes aware of a personal data breach, the controller shall notify the supervisory authority within 72 hours, else the controller shall provide reasons for the delay.“ 
            Example 2:
                „The room-service manager at The Evanstonian takes down the order when a guest calls room service.“
                -> If a guest calls room service, the room-service manager at takes down the order.
                    Reasons:
                    - „The Evanstonian“ is the company and is not relevant for the activity. It represents meta information.

    If process steps can be done in parallel start the sentence with „Meanwhile, ….“.
            Example:
            "The ongoing repair consists of two activities, which are executed, in an arbitrary order. The first activity is to check and repair the hardware, whereas the second activity checks and configures the software."
            -> "The Computer Repair Service (CRS) checks and repairs the hardware. In the meanwhile, the Computer Repair Service (CRS) checks and configures the software."
    """)

    # Implict Actions
    prompts.append("""
            ### Instuction: #### \n
            Some sentences use implicit ACTIONS, also try to extract this information and make it explicit in the sentence format explained in Step 2.
            Example 1:
                „Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results.“
                    ->  „Documented information shall be available as evidence of the implementation of the audit programme(s) and the audit results.“
                -> implies the ACTION „document the results“.

            Example 2:
                "The Room Service Manager then submits an order ticket to the kitchen to begin preparing the food."
                -> „The Room Service Manager submits an order ticket to the kitchen. The kitchen prepares the food.“
                Make sure to keep the order of the sentences and to explicitly name the ACTOR and the ACTION.
        """)
    # Resolve References
    prompts.append("""
            ### Instuction: #### \n
            Resolve references:
            Examples:
            -> "she, he, it, they" refer to an actor. Try to replace the reference with the name of the actor.
            -> "this, that" refer to an object. Try to replace the reference with the name of the object.
            -> "these, those" refer to multiple objects. Try to replace the reference with the name of the objects.
        """)
    prompts.append("""
                ### Instuction: #### \n
                Make sure all ACTIONs and Actors are from the inital original text and nothing was added.
            """)

    def generate_response(prompt):
        # Get the response from GPT-3
        model_engine = "text-davinci-003"
        if debug_mode: print(f"*** Prompt:  ****  len: {len(prompt).__str__()} \n" + prompt)
        response = openai.Completion.create(
            engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.0)
        # Extract the response from the response object
        response_text = response["choices"][0]["text"]
        text_response = response_text.strip()
        if debug_mode: print("*** Response:  **** \n" + text_response)
        return text_response

    # definition of the main function
    def my_chatbot(input: doc, history=None):
        if not history:
            history = []
        prompt = ""
        for dic in history:
            prompt += "Human: " + dic["human"] + "\n"
            prompt += "AI: " + dic["ai"] + "\n"
        # add current input to the prompt
        prompt += "Human: " + input + "\n"
        prompt += "AI: "
        prompt = intro + prompt
        response = generate_response(prompt)
        history.append({"human": input, "ai": response})
        return response, history

    history = []
    query = inital_prompt + doc.text
    response, history = my_chatbot(query, history)
    for sent in doc.sents:
        response = sent.text
        for prompt in prompts:
            query = prompt + response
            # print("Number of characters:" + len(query).__str__())
            response, history = my_chatbot(query, history)
    return response

input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text7.txt"
text_input = open(input_path, 'r').read().replace('\n', ' ')
nlp = spacy.load('en_core_web_trf')
doc = nlp(text_input)
print(preprocess_text_with_LLM(doc))
