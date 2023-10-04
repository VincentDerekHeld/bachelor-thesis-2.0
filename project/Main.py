import BPMNStarter


def run__all_texts():
    from project import BPMNStarter
    itaration = 11
    while itaration < 23:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text_vh" + itaration.__str__() + "with_more_actors-with_and_opartor.png"
        title = "Text" + itaration.__str__()
        BPMNStarter.start_task(input_path, title, output_path)
        itaration += 1


if __name__ == '__main__':
    #run__all_texts()
    input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text6.txt"
    BPMNStarter.start_task(input_path, "example", "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text6_mod3.png", debug=False)
