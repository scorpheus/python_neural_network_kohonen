__author__ = 'scorpheus'

import sys
from node import Node
from physic_world import PhysicWorld

import KohonenBehaviour

# from node_1_input_move_backward_stop_forward.node_input_1_input_dist_front import NodeInputs
# from node_1_input_move_backward_stop_forward.action_3_backward_stop_forward import Actions
# from node_1_input_move_backward_stop_forward.decision_maker import DecisionMaker

from node_2_inputs_move_right_left_wheel.node_input_2_input_dist_front_right_left import NodeInputs
from node_2_inputs_move_right_left_wheel.action_4_move_right_left_wheel import Actions
from node_2_inputs_move_right_left_wheel.decision_maker import DecisionMaker

# from node_2_inputs_move_right_left_wheel_new_decision.node_input_2_input_dist_front_right_left import NodeInputs
# from node_2_inputs_move_right_left_wheel_new_decision.action_4_move_right_left_wheel import Actions
# from node_2_inputs_move_right_left_wheel_new_decision.decision_maker import DecisionMaker

# import and init OOKPY
import gs
import gs.plus.clock as clock
import gs.plus.input as input
import gs.plus.render as render
import gs.plus.camera as camera

render.init(640, 480, "pkg.core")
fps = camera.fps_controller(0, 15, 0)

array_perso = []
# init perso

for i in range(5):
	perso_inputs = NodeInputs()
	perso_actions = Actions()
	perso_decision_maker = DecisionMaker()
	perso = Node(perso_actions, perso_inputs, perso_decision_maker)
	array_perso.append(perso)

physic_world = PhysicWorld(gs.Vector2(640, 480))

#input handling (somewhat boilerplate code):
def play_simulation():
	while not input.key_press(gs.InputDevice.KeyEscape):
		clock.update()
		fps.update(clock.get_dt())
		render.set_camera3d(fps.pos.x, fps.pos.y, fps.pos.z, fps.rot.x, fps.rot.y, fps.rot.z)

		render.clear()

		for perso in array_perso:
			perso.draw()
			perso.update(physic_world)

		array_perso[0].kohonen_behaviour.draw(render.get_renderer().GetCurrentOutputWindow().GetSize().x, render.get_renderer().GetCurrentOutputWindow().GetSize().y)


		physic_world.draw()

		# render text
		if input.key_down(gs.InputDevice.KeyL):
			render.text2d(10, 120, 'Frag in Mem: %d' % KohonenBehaviour.memory.GetNbFragment())
			for action in range(perso_actions.nb_actions):
				render.text2d(10, 140 + 20*action, 'Frag for %s: %d, %d%%' % (perso_actions.get_current_action_name(action), KohonenBehaviour.memory.m_NbFragmentPerActionArray[action], KohonenBehaviour.memory.m_TabPercentFragmentPerAction[action]), 12, array_perso[0].kohonen_behaviour.color_array[action])

		render.text2d(10, 50, str(perso.selected_action)+" "+perso_actions.get_current_action_name(perso.selected_action))

		#draw it to the screen
		render.flip()

if __name__ == "__main__":
	play_simulation()