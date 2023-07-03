from typing import Optional

from processpiper import ProcessMap, EventType, ActivityType, GatewayType
from processpiper.text2diagram import render

from Structure.Activity import Activity
from Structure.Block import ConditionBlock, AndBlock, ConditionType
from Structure.Structure import Structure


def create_bpmn_model(structure_list: [Structure], actor_list: list, title: str, save_path: str,
                      theme: str = "BLUEMOUNTAIN"):
    input_syntax = create_bpmn_description(structure_list, actor_list, title, theme=theme)
    print(input_syntax)
    # render_bpmn_model(input_syntax, save_path)
    print("debug model --> omit the rendering")


def render_bpmn_model(input_syntax: str, path: str):
    render(input_syntax, path)


def create_bpmn_description(structure_list: [Structure], actor_list: list, title: str,
                            theme: str = "BLUEMOUNTAIN") -> str:
    result = ""
    result += "title: " + title + "\n"
    result += "width: " + str(10000) + "\n"
    result += "colourtheme: " + theme + "\n"

    lanes = {}
    connections = []

    if len(actor_list) < 2:
        lanes["dummy"] = []
    else:
        for actor in actor_list:
            lanes[actor] = []

    key = None
    connection_id = 0
    last_gateway = None
    for structure in structure_list:
        if structure_list.index(structure) == 0:
            key = belongs_to_lane(structure_list, lanes, structure, key)
            lanes[key].append("(start) as start")
            connections.append("start")

        if isinstance(structure, Activity):
            key = belongs_to_lane(structure_list, lanes, structure, key)
            append_to_lane(key, lanes, connection_id, connections, structure, last_gateway)
        elif isinstance(structure, ConditionBlock):
            end_gateway = "gateway_" + str(structure.id) + "_end"

            if len(structure.branches[0]["condition"]) > 0:
                key = belongs_to_lane(structure_list, lanes, structure.branches[0]["condition"][0], key)
            append_to_lane(key, lanes, connection_id, connections, structure, last_gateway)

            for branch in structure.branches:
                connection_id += 1
                if structure.is_simple() and branch["type"] == ConditionType.IF:
                    connections.append("gateway_" + str(structure.id) + '-"yes"')
                elif structure.is_simple() and branch["type"] == ConditionType.ELSE:
                    connections.append("gateway_" + str(structure.id) + '-"no"')
                else:
                    condition = ""
                    for c in branch["condition"]:
                        condition += str(c)
                        if branch["condition"].index(c) != len(branch["condition"]) - 1:
                            condition += ", "
                    # if condition == "None":
                    #     condition = ""
                    connections.append("gateway_" + str(structure.id) + '-"' + condition + '"')

                need_end_gateway = True
                for activity in branch["actions"]:
                    key = belongs_to_lane(structure_list, lanes, activity, key)
                    append_to_lane(key, lanes, connection_id, connections, activity, last_gateway)
                    if activity.is_end_activity:
                        need_end_gateway = False
                        end_id = "end_" + str(activity.id)
                        early_end_gateway = "(end) as end_" + str(activity.id)
                        lanes[key].append(early_end_gateway)
                        connections[connection_id] += "->" + end_id
                        continue

                if need_end_gateway:
                    connections[connection_id] += "->" + end_gateway

            lanes[key].append("<> as " + end_gateway)
            connection_id += 1
            last_gateway = end_gateway
        elif isinstance(structure, AndBlock):
            end_gateway = "gateway_" + str(structure.id) + "_end"

            append_to_lane(key, lanes, connection_id, connections, structure, last_gateway)

            for branch in structure.branches:
                connection_id += 1
                connections.append("gateway_" + str(structure.id))
                for activity in branch:
                    key = belongs_to_lane(structure_list, lanes, activity, key)
                    append_to_lane(key, lanes, connection_id, connections, activity, last_gateway)
                connections[connection_id] += "->" + end_gateway

            lanes[key].append("<@parallel> as " + end_gateway)
            connection_id += 1
            last_gateway = end_gateway

        if structure.is_end_activity:
            lanes[key].append("(end) as end")
            if connection_id < len(connections):
                connections[connection_id] += "->end"
            else:
                connections.append(last_gateway)
                connections[connection_id] += "->end"

    for lane in lanes:
        if lane == "dummy":
            result += "lane: \n"
        else:
            result += "lane: " + lane + "\n"

        for element in lanes[lane]:
            result += "\t" + element + "\n"

    result += "\n"

    for connection in connections:
        result += connection + "\n"

    return result


def find_next_id(structure_list: [Structure], structure: Structure) -> str:
    index = structure_list.index(structure)
    if index + 1 < len(structure_list):
        if isinstance(structure_list[index + 1], Activity):
            return "activity_" + str(structure_list[index + 1].id)
        elif isinstance(structure_list[index + 1], ConditionBlock):
            return "gateway_" + str(structure_list[index + 1].id)
        elif isinstance(structure_list[index + 1], AndBlock):
            return "gateway_" + str(structure_list[index + 1].id)
    else:
        return "end"


def append_to_lane(key: str, lanes: {}, connection_id: int, connections: list, structure: Structure,
                   last_gateway: Optional[str]):
    if isinstance(structure, Activity):
        if structure.process.actor is not None:
            if structure.process.actor.full_name in lanes.keys():
                lanes[key].append("[" + str(structure.process.action) + "] as activity_" + str(structure.id))
            else:
                # todo: develop a better toString method for visualization
                lanes[key].append(
                    "[" + str(structure.process.actor) + " " + str(structure.process.action) + "] as activity_" +
                    str(structure.id))
        else:
            lanes[key].append(
                "[" + str(structure.process.action) + "] as activity_" + str(structure.id))
    elif isinstance(structure, ConditionBlock):
        if structure.is_simple():
            condition = structure.branches[0]["condition"][0]
            if condition is not None:
                lanes[key].append("<" + str(condition) + "?> as gateway_" + str(structure.id))
            else:
                lanes[key].append("<> as gateway_" + str(structure.id))
        else:
            lanes[key].append("<> as gateway_" + str(structure.id))
    elif isinstance(structure, AndBlock):
        lanes[key].append("<@parallel> as gateway_" + str(structure.id))

    if isinstance(structure, Activity):
        connection_name = "activity_" + str(structure.id)
    else:
        connection_name = "gateway_" + str(structure.id)

    if connection_id > len(connections) - 1:
        if last_gateway is not None:
            connections.append(last_gateway)
            connections[connection_id] += "->" + connection_name
        else:
            connections.append(connection_name)
    else:
        connections[connection_id] += "->" + connection_name


def belongs_to_lane(activity_list: [Structure], lanes: {}, structure: Structure, previous_actor: Optional[str]) -> str:
    if len(lanes) == 1:
        return "dummy"

    if previous_actor is None:
        for activity in activity_list:
            if activity.process.actor is not None:
                if activity.process.actor.full_name in lanes.keys():
                    return activity.process.actor.full_name
    else:
        if structure.process.actor is None:
            return previous_actor
        else:
            if structure.process.actor.full_name in lanes.keys():
                return structure.process.actor.full_name
            else:
                return previous_actor
