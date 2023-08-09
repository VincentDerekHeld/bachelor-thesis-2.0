from processpiper.text2diagram import render

if __name__ == '__main__':
    input_syntax = """
title: result19_LLM
width: 10000
colourtheme: BLUEMOUNTAIN
lane: sales department
	[confirm the order] as activity_6
	[emit an invoice] as activity_7
	[wait for the payment] as activity_8
	[complete the order archival] as activity_10
	[confirm the purchase order] as activity_17
	[archive the purchase order] as activity_18
	(end) as end
lane: warehouse & distribution
    (start) as start
	[check the purchase order] as activity_2
	<is the product in stock?> as gateway_1
	[retrieve the product] as activity_5
	[ship the product] as activity_9
	<> as gateway_1_end
	[check the raw materials availability] as activity_11
	[access the suppliers catalog] as activity_12
	[obtain the raw materials] as activity_13
	[manufacture the product] as activity_15
	[complete the manufacturing process] as activity_16

start->activity_2->gateway_1->activity_5->activity_6->activity_7->activity_8->activity_9->activity_10->gateway_1_end
gateway_1->activity_11->activity_12->activity_13->activity_15->activity_16->gateway_1_end
gateway_1_end->activity_17->activity_18->end
       """
    render(input_syntax, "/Users/shuaiwei_yu/Desktop/bachelor-thesis/project/Diagram/output_LLM/text19_bpmn.png")
