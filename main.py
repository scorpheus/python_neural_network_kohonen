__author__ = 'scorpheus'

import sys
from node import Node

from node_1_input_move_backward_stop.node_input_1_input_dist_front import NodeInputs
from node_1_input_move_backward_stop.action_2_backward_stop import Actions
from node_1_input_move_backward_stop.decision_maker import DecisionMaker

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