from processpiper.text2diagram import render

if __name__ == '__main__':
    input_syntax = """
title: result05_LLM_generation
width: 10000
colourtheme: BLUEMOUNTAIN
lane: Mail Processing Unit
(start) as start
[collect mail] as activity_1
[sort unopened mail into various business areas] as activity_2
[distribute mail] as activity_3

lane: Registry
[receive mail] as activity_4
[open and sort mail into groups for distribution] as activity_5
[register in a manual incoming Mail Register] as activity_6
[Assistant Registry Manager performs a quality check] as activity_7
<compliant?> as gateway_1
[compile a list of requisition explaining the reason for rejection] as activity_8
[send back list to the party] as activity_9
<> as gateway_1_end
[capture the matter details] as activity_10
[provide matter details to the Cashier] as activity_11
[put the receipt and copied documents into an envelope] as activity_12
[post envelope to the party] as activity_13

lane: Cashier
[take the applicable fees] as activity_14
[capture the Party Details] as activity_15
[print the Physical Court File] as activity_16
(end) as end

start->activity_1->activity_2->activity_3->activity_4->activity_5->activity_6->activity_7->gateway_1
gateway_1-"no"->activity_8->activity_9->gateway_1_end
gateway_1-"yes"->activity_10->activity_11->activity_14->activity_12->activity_13->gateway_1_end
gateway_1_end->activity_15->activity_16->end
       """
    render(input_syntax, "/Users/shuaiwei_yu/Desktop/bachelor-thesis/project/Diagram/output_LLM/text05_bpmn_gen.png")
