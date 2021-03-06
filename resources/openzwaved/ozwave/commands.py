import logging
import time
import globals,utils
import threading
from ozwave.utilities.Constants import *
import node_utils,value_utils

def send_command_zwave(_node_id, _cc_id, _instance_id, _index, _value):
	logging.info("Send command to node "+str(_node_id)+" on class "+str(_cc_id)+" instance "+str(_instance_id)+" index "+str(_index)+" value "+str(_value))
	utils.check_node_exist(_node_id)
	if _cc_id == COMMAND_CLASS_NO_OPERATION:
		return node_utils.test_node(_node_id, 1)
	if _cc_id == COMMAND_CLASS_ASSOCIATION or _cc_id == COMMAND_CLASS_WAKE_UP:
		return
	for value_id in globals.network.nodes[_node_id].get_values(class_id=_cc_id, genre='All', type='All', readonly=False, writeonly='All'):
		if globals.network.nodes[_node_id].values[value_id].instance - 1 == _instance_id and (_index is None or globals.network.nodes[_node_id].values[value_id].index == _index):
			value = globals.network.nodes[_node_id].values[value_id].check_data(_value)
			globals.network.nodes[_node_id].values[value_id].data = value
			if globals.network.nodes[_node_id].values[value_id].genre == 'System':
				value_utils.mark_pending_change(globals.network.nodes[_node_id].values[value_id], value)
			return True
	raise Exception('Value not found')