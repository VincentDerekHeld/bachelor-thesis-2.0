import os
import pprint
import openai

def context_str(docs):
  s=""
  for i, d in enumerate(docs):
    s+=f"Document {i}:"
    s+="\n"
    s+=d.page_content
    s+="\n\n"
  return s

def pretty_print(docs):
  print(context_str(docs))

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"
openai.organization = "org-cGUe4rwtHg1jEuK4T5Ya9rU3"

# generate a response of an llm (open-ai) given a prompt
def generate_response(prompt):
    # Get the response from GPT-3
    model_engine = "text-davinci-003"

    response = openai.Completion.create(
        engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.0)

    # Extract the response from the response object
    response_text = response["choices"][0]["text"]

    text_response = response_text.strip()

    return text_response

# definition of the main function
def my_chatbot(input, history=None):
    if not history:
      history = []

    # create the prompt
    prompt = ""

    # add history
    for dic in history:
      prompt += "Human: "+dic["human"]+"\n"
      prompt += "AI: "+dic["ai"]+"\n"

    # add current input to the prompt
    prompt += "Human: "+input+"\n"
    prompt += "AI: "

    # truncate prompt
    prompt = prompt[:4000]

    # add introduction to prompt
    intro = "You are a chatty chatbot.\n"
    prompt = intro+prompt

    response = generate_response(prompt)
    history.append({"human": input, "ai":response})
    return response, history

# set chat to True in order to start the chat
chat = True
if chat:
    exit_conditions = ("quit", "exit")
    history = []
    while True:
        query = input("Human: ")
        if query in exit_conditions:
            break
        else:
          response, history = my_chatbot(query,history)
          print(f"AI: {response}")