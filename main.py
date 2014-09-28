__author__ = 'scorpheus'

import sys
from node import Node

from physic_world import PhysicWorld

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
perso_inputs = NodeInputs()
perso_actions = Actions()
perso_decision_maker = DecisionMaker()
perso = Node(perso_actions, perso_inputs, perso_decision_maker)

physic_world = PhysicWorld(window)

# initialize font
myfont = pygame.font.SysFont("monospace", 15)
clock = pygame.time.Clock()

#input handling (somewhat boilerplate code):
def play_simulation():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			# else:
			# 	print(event)

		window.fill((0,0,0))
		perso.draw(pygame.draw, window)
		perso.update(physic_world)

		# render text
		label = myfont.render(str(perso.selected_action)+" "+perso_actions.get_current_action_name(perso.selected_action), 1, (255,255,0))
		window.blit(label, (10, 100))
		clock.tick()
		label = myfont.render("fps: "+str(int(clock.get_fps())), 1, (255,255,0))
		window.blit(label, (10, 50))

		physic_world.draw(pygame.draw, window)

		#draw it to the screen
		pygame.display.flip()

if __name__ == "__main__":
	play_simulation()