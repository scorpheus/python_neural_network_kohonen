import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
options = {
    'build_exe': {
        'compressed': True,
		'include_files': ['pkg.core/', 'node_2_inputs_move_right_left_wheel/', 'actions.py', 'decision_maker.py', 'node_inputs.py', 'vector_helper.py']
    }
}

setup(  name = "AI",
        version = "0.1",
        description = "Kohonen network",
        options = options,
        executables = [Executable("main.py")])