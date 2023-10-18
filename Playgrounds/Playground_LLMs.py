import os
import openai

openai.api_key = "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"
openai.organization = "org-cGUe4rwtHg1jEuK4T5Ya9rU3"
# print(openai.Model.list())

promt: str = """Parse the following process description carefully by extracting only the process-relevant steps. 
-> Do only return the answer without adding any extra information or interpretation.
Example: do not add: „Following the provided instructions, here are the extracted process-relevant steps:“
Try to return a text of short precise sentences, which contains only the process relevant information Follow carefully the following instructions and solve the tasks sentence for sentence.
1. Decide if the information is relevant for the process. Introductions are not relevant. The only information we are interested in are real process steps.
	-> If yes, go one. 
	-> If not, do not use this information for the output.
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
5. For the identification of the ACTOR, keep in mind, a actor can  for e.g. be a natural person, a organization, such as a company or a department, but sometimes also a device or a system can be an valide Actor. 
6. The output has to contain full sentences and can not contain list items, such as bullet points.

TEXT:

"""

input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text10_GPT4.txt"
text_input = open(input_path, 'r').read().replace('\n', ' ')
promt += text_input

content: str = promt

print("Request: \n \t" + content)
messages = [{"role": "user", "content": content}]
messages.append({"role": "system",
                 "content": "You are a process analyst, that wants to simplyfiy the textual description of a process."})


completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)
chat_response: str = completion.choices[0].message.content
messages.append({"assistant": "system", content: chat_response}) #store the response in the messages list to achieve a message history

print(chat_response)

# org-id = org-cGUe4rwtHg1jEuK4T5Ya9rU3



