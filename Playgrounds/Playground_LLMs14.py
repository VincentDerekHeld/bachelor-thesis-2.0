import os
import requests
import spacy

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def preprocess_text_with_LLM(doc):
    debug_mode = True
    prompts = []
    outro = """\n ### TEXT ### \n"""
    answer_outro = "\n ### Answer / Response: ###"
    prompt_first = ("""
    Carefully extract action items and actors from this text and return the result carefully as grammatical complete sentences with the following structure:
    ([condition])[article of actor and actor] [action item] ([else clause]).
    """)

    def generate_response(prompt) -> str:
        try:
            if debug_mode: print(f"*** Prompt: *** len: {len(prompt).__str__()} \n {prompt} \n")
            api_key = os.environ["OPENAI_API_KEY"]
            # Define the headers for the HTTP request
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            # Define the data payload for the API request
            data = {
                "model": "gpt-3.5-turbo-instruct",
                "prompt": prompt,
                "max_tokens": 1500,
                "temperature": 0
            }
            # Make the POST request to the OpenAI API
            response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
            # Extract the response text
            response_data = response.json()
            response_text = response_data['choices'][0]['text'].strip() if response_data['choices'] else "No response"
            response_text = response_text.strip()
            if debug_mode:
                print(f"*** Response: ***\n {response_text}")
                print("*" * 50)
            return response_text
        except requests.exceptions.Timeout:
            # Handle timeout specifically
            if debug_mode:
                print("Request timed out")
            return "Request timed out"
        except Exception as e:
            # Handle any other exceptions
            if debug_mode:
                print(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"

    # Initital Instructions and
    result = ""
    query = prompt_first + outro + doc.text + answer_outro
    current_sent = generate_response(query)
    result = result + " " + current_sent + "\n"

    print("**** Full description: **** \n" + result.strip().replace("\n", " ").replace(".", ". ").replace("!",
                                                                                                          "! ").replace(
        "?", "? "))
    return result.strip()


def write_to_file(number: int, nlp):
    input_path = f"/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text{number.__str__()}.txt"
    text_input = open(input_path, 'r').read().replace("\n", " ")
    doc = nlp(text_input)
    content = preprocess_text_with_LLM(doc)
    output_path = f"/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Approach-14/Text{number.__str__()}.txt"
    with open(output_path, 'w') as file:
        file.write(content)
    print(f"Created Text: {number.__str__()}")


nlp = spacy.load('en_core_web_trf')
for i in range(6, 10):
   write_to_file(i, nlp)
#write_to_file(1, nlp)
