__author__ = 'scorpheus'

import sys
from node import Node

# from node_1_input_move_backward_stop_forward.node_input_1_input_dist_front import NodeInputs
# from node_1_input_move_backward_stop_forward.action_3_backward_stop_forward import Actions
# from node_1_input_move_backward_stop_forward.decision_maker import DecisionMaker

from node_2_inputs_move_right_left_wheel.node_input_2_input_dist_front_right_left import NodeInputs
from node_2_inputs_move_right_left_wheel.action_4_move_right_left_wheel import Actions
from node_2_inputs_move_right_left_wheel.decision_maker import DecisionMaker


#import and init pygame
import pygame
pygame.init()

#create the screen
window = pygame.display.set_mode((640, 480))
pouipouin_inputs = NodeInputs()
pouipouin_actions = Actions()
pouipouin_decision_maker = DecisionMaker()
pouinpouin = Node(pouipouin_actions, pouipouin_inputs, pouipouin_decision_maker)

#input handling (somewhat boilerplate code):
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		# else:
		# 	print(event)

	window.fill((0,0,0))
	pouinpouin.draw(pygame.draw, window)
	pouinpouin.update()

	#draw it to the screen
	pygame.display.flip()