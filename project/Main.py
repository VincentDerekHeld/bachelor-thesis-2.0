import BPMNStarter
from project.Constant import DEBUG


def run__all_texts():
    itaration = 11
    while itaration < 24:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text" + itaration.__str__() + "_baseline_approach.png"
        title = "Text" + itaration.__str__() + "baseline approach"
        BPMNStarter.start_task(input_path, title, output_path, debug=DEBUG)
        itaration += 1


def run__setof_texts():
    itaration = 1
    while itaration < 24:
        if itaration in [7]:
            input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
            output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text" + itaration.__str__() + "_GPT4.png"
            title = "Text" + itaration.__str__() + "own approach"
            BPMNStarter.start_task(input_path, title, output_path, debug=DEBUG)
        itaration += 1


def run__set_of_texts_GPT():
    itaration = 1
    while itaration < 24:
        if itaration in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]:
            input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Approach-15/Text" + itaration.__str__() + ".txt"
            output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Approach-19/Text" + itaration.__str__() + ".png"
            title = "Text" + itaration.__str__()
            BPMNStarter.start_task(input_path, title, output_path, debug=DEBUG)
        itaration += 1


def run_approach15xPaper():
    for i in range(31, 96):
        try:
            input_path = f"/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Approach-15xPaper/LLM_preprocessed_text/Text{i}.txt"
            output_path = f"/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Approach-15xPaper/Output/our_model_{i}.png"
            title = f"Text {i}: our model"
            BPMNStarter.start_task(input_path, title, output_path, debug=DEBUG)
        except:
            print(f"Text {i} failed")


if __name__ == '__main__':
    # run__set_of_texts_GPT()
    run_approach15xPaper()
    # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    # [1, 3, 4, 5, 6, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    """input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text6.txt"
    BPMNStarter.start_task(input_path, "example",
                           "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text6_mod3.png",
                           debug=True)"""

# Approach 18: uses input of Approach 15 with analyze_document_vh1
# Approach 19: uses input of Approach 15 with analyze_document

# Approach 20: uses input of Approach 15 with get valid actors vh1
# Approach 21: uses input of Approach 15 with get valid actors
