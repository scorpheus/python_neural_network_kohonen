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


# import and init OOKPY
from gs.plus import *

render.init(640, 480, "pkg.core")

# init perso
perso_inputs = NodeInputs()
perso_actions = Actions()
perso_decision_maker = DecisionMaker()
perso = Node(perso_actions, perso_inputs, perso_decision_maker)

physic_world = PhysicWorld(gs.Vector2(640, 480))

# create the font object
font = gs.RasterFont("@core/fonts/default.ttf", 12, 512)


#input handling (somewhat boilerplate code):
def play_simulation():
	while not key_press(gs.InputDevice.KeyEscape):

		render.clear()

		perso.draw(render)
		perso.update(physic_world)

		render.renderer.EnableBlending(True)
		render.renderer.EnableDepthTest(False)

		# render text
		if key_down(gs.InputDevice.KeyL):
			font.Write(render.render_system, 'Frag in Mem: %d' % perso.kohonen_behaviour.memory.GetNbFragment(), gs.Vector3(10, 120, 0.5))
			for action in range(perso_actions.nb_actions):
				font.Write(render.render_system, 'Frag for %s: %d, %d%%' % (perso_actions.get_current_action_name(action), perso.kohonen_behaviour.memory.m_NbFragmentPerActionArray[action], perso.kohonen_behaviour.memory.m_TabPercentFragmentPerAction[action]), gs.Vector3(10, 140 + 20*action, 0.5),
						   perso.kohonen_behaviour.color_array[action])

		font.Write(render.render_system, str(perso.selected_action)+" "+perso_actions.get_current_action_name(perso.selected_action), gs.Vector3(10, 50, 0.5))

		physic_world.draw(render)

		#draw it to the screen
		render.render_system.DrawRasterFontBatch()
		render.flip()

if __name__ == "__main__":
	play_simulation()