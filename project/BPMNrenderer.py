from processpiper.text2diagram import render

if __name__ == '__main__':
    input_syntax = """
title: result15
width: 20000
colourtheme: BLUEMOUNTAIN
lane: customer
	(start) as start
	[a switch over request initiate the process] as activity_22
	[transmits his data] as activity_23
	<the customer not exist in the customer data base?> as gateway_3
	[create a new customer object in case] as activity_5
	[a new customer object remain during the rest of the process flow] as activity_6
	<> as gateway_3_end
	[this object consists of data elements] as activity_32
	[use the generated customer object in combination with other customer data] as activity_33
	[prepare the contract documents for the power supplier switch] as activity_34
	[carry an automated check of the contract documents the following out in] as activity_35
	[confirm their successful generation] as activity_36
	[analyze the causing issues in case of a negative response] as activity_37
	[resolve the causing issues] as activity_38
	[case of a negative response not generate the contract documents] as activity_39
	[generate the contract documents] as activity_40
	<send a confirmation document case of a positive response out to?> as gateway_7
	[execute the switch over to the new supplier] as activity_9
	<> as gateway_7_end
lane: customer service
	[is] as activity_24
	[receive the customer data] as activity_25
	[enter a customer data object] as activity_26
	[enter customer data] as activity_27
	[compare it with the internal customer data base] as activity_28
	[check it for completeness and plausibility] as activity_29
	<correct these case of any errors on?> as gateway_1
	<> as gateway_1_end
	[do the comparison of data] as activity_30
	[store individual customer data] as activity_31
	[creates a cis contract] as activity_46
	<> as gateway_16
	[confirm contract] as activity_17
	[withdraw from the switch contract] as activity_18
	<> as gateway_16_end
	<> as gateway_19
	[the process flow at customer service continue] as activity_20
	[the process flow at customer service ends] as activity_21
	<> as gateway_19_end
	[regard the contract] as activity_47
	[the process continues] as activity_48
	[the confirmation message by the customer is not necessary] as activity_49
	[message speed up the switch process] as activity_50
	[the grid operator the switch date transmits the power meter data via] as activity_51
	[power supply begun] as activity_52
	[the grid operator at the same time computes the final billing] as activity_53
	[the grid operator send billing] as activity_54
	[imports the meter data] as activity_58
	[receiving the meter data] as activity_59
	[systems require the information] as activity_60
	[the process of winning a new customer ends] as activity_61
	[winning a new customer] as activity_62
	(end) as end
lane: cis
	[send a request to the grid operator] as activity_41
lane: selected supplier
	<the selected supplier supply the customer in the future?> as gateway_10
	[request puts the question] as activity_12
	<> as gateway_10_end
	[the grid operator check the switch over request for supplier concurrence] as activity_42
	[the grid operator transmits a response comment] as activity_43
	<> as gateway_13
	<> as gateway_13_end
	[the grid operator communicates with the old supplier] as activity_44
	[the grid operator carry out the termination of the sales agreement between the customer and the old supplier] as activity_45
lane: old supplier
	[creates the final billing] as activity_55
	[send the final billing] as activity_56
	[the process ends] as activity_57

start->activity_22->activity_23->activity_24->activity_25->activity_26->activity_27->activity_28->activity_29->gateway_1
gateway_1-"yes"->gateway_1_end
gateway_1-"no"->gateway_1_end
gateway_1_end->activity_30->activity_31->gateway_3
gateway_3-"yes"->activity_5->activity_6->gateway_3_end
gateway_3-"no"->gateway_3_end
gateway_3_end->activity_32->activity_33->activity_34->activity_35->activity_36->activity_37->activity_38->activity_39->activity_40->gateway_7
gateway_7-"yes"->activity_9->gateway_7_end
gateway_7-"no"->gateway_7_end
gateway_7_end->activity_41->gateway_10
gateway_10-"yes"->activity_12->gateway_10_end
gateway_10-"no"->gateway_10_end
gateway_10_end->activity_42->activity_43->gateway_13
gateway_13-"the grid operator demand the resolution of the conflict"->gateway_13_end
gateway_13-"the grid operator in the case of supplier concurrence inform all involved suppliers"->gateway_13_end
gateway_13_end->activity_44->activity_45->activity_46->gateway_16
gateway_16-""->activity_17->gateway_16_end
gateway_16-""->activity_18->gateway_16_end
gateway_16_end->gateway_19
gateway_19-""->activity_20->gateway_19_end
gateway_19-""->activity_21->gateway_19_end
gateway_19_end->activity_47->activity_48->activity_49->activity_50->activity_51->activity_52->activity_53->activity_54->activity_55->activity_56->activity_57->activity_58->activity_59->activity_60->activity_61->activity_62->end

    """
    render(input_syntax, "/Users/shuaiwei_yu/Desktop/output/text15_bpmn.png")
