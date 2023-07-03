from processpiper.text2diagram import render

if __name__ == '__main__':
    input_syntax = """
title: debug
width: 10000
colourtheme: BLUEMOUNTAIN
lane: sales department
	(start) as start
	[receives an order] as activity_7
	[create a new process instance] as activity_8
	<@parallel> as gateway_1
	[repeat this procedure for each item on the part list] as activity_2
lane: engineering department
	[the meantime prepares everything for] as activity_3
	<@parallel> as gateway_1_end
	<@parallel> as gateway_4
lane: member
	[accept the order for a customized bike] as activity_5
	[reject the order for a customized bike] as activity_6
	<@parallel> as gateway_4_end
	(end) as end

start->activity_7->activity_8->gateway_1
gateway_1->activity_2->gateway_1_end
gateway_1->activity_3->gateway_1_end
gateway_1_end->gateway_4
gateway_4->activity_5->gateway_4_end
gateway_4->activity_6->gateway_4_end
gateway_4_end->end
    """
    render(input_syntax, "/Users/shuaiwei_yu/Desktop/output/text00_test.png")
