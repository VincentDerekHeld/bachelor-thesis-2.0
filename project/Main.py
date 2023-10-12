import BPMNStarter


def run__all_texts():
    from project import BPMNStarter
    itaration = 23
    while itaration < 24:
        input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
        output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text_vh" + itaration.__str__() + "with_more_actors-with_and_opartor.png"
        title = "Text" + itaration.__str__()
        BPMNStarter.start_task(input_path, title, output_path, debug=True)
        itaration += 1


def run__setof_texts():
    from project import BPMNStarter
    itaration = 1
    while itaration < 24:
        if itaration in [7]:
            input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text" + itaration.__str__() + ".txt"
            output_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text_vh" + itaration.__str__() + "_new2.png"
            title = "Text" + itaration.__str__() + "Extraction-VH"
            BPMNStarter.start_task(input_path, title, output_path, debug=True)
        itaration += 1


if __name__ == '__main__':
    run__setof_texts()
    #[1, 3, 4, 5, 6, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    #run__all_texts()
    # 2, 7, 9,10,
    """input_path = "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/project/Text/text_input_vh/Text6.txt"
    BPMNStarter.start_task(input_path, "example",
                           "/Users/vincentderekheld/PycharmProjects/bachelor-thesis/Evaluation/Text6_mod3.png",
                           debug=True)"""
