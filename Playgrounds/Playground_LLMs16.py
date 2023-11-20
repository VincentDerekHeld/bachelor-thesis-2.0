import os
import requests
import spacy

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def preprocess_text_with_LLM(doc):
    debug_mode = False
    prompts = []
    outro = """\n ### TEXT ### \n"""
    answer_outro = "\n ### Answer / Response: ###"
    prompt_first = ("""
    Carefully determine if the following text is a description of a process or a regulatory document / norm.
    1) If the text is a description of a process, please write "process" in the text field below.
    2) If the text is a regulatory document / norm, please write "regulatory document / norm" in the text field below.
    """)
    prompt_second = ("""
       Carefully determine if the following text is a description of a process or a regulatory document / norm.
       1) If the text is a description of a process, please write "process" in the text field below and give a reason why you think so.
       2) If the text is a regulatory document / norm, please write "regulatory document / norm" in the text field below give a reason why you think so.
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
    query = prompt_second + outro + doc.text + answer_outro
    current_sent = generate_response(query)
    result = result + " " + current_sent + "\n"
    return result.strip()


def write_to_file(number: int, nlp):
    input_path = f"/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text{number.__str__()}.txt"
    text_input = open(input_path, 'r').read().replace("\n", " ")
    doc = nlp(text_input)
    content = preprocess_text_with_LLM(doc)
    print(f" Text {number.__str__()}: {content}")


nlp = spacy.load('en_core_web_trf')
for i in range(1, 24):
    write_to_file(i, nlp)
# write_to_file(1, nlp)
