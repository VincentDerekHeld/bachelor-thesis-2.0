import os
import openai


def preprocess_text_with_LLM(text_input):
    prompts = []
    prompts.append("""
        """)

    def generate_response(prompt):
        model_engine = "text-davinci-003"
        response = openai.Completion.create(
            engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.0)
        response_text = response["choices"][0]["text"]
        text_response = response_text.strip()
        return text_response

    # definition of the main function
    def my_chatbot(input, history=None):
        if not history:
            history = []
        prompt = ""
        for dic in history:
            prompt += "Human: " + dic["human"] + "\n"
            prompt += "AI: " + dic["ai"] + "\n"
        # add current input to the prompt
        prompt += "Human: " + input + "\n"
        prompt += "AI: "
        intro = """Intro Text"""
        response = generate_response(intro + prompt)
        history.append({"human": input, "ai": response})
        return response, history

    history = []
    response = text_input
    for promt in prompts:
        response, history = my_chatbot(promt + response, history)
    return response

input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text6.txt"
text_input = open(input_path, 'r').read().replace('\n', ' ')
print(preprocess_text_with_LLM(text_input))
