from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import main

graphviz = GraphvizOutput()
graphviz.output_file = 'basic.png'

with PyCallGraph(output=graphviz):
	main.play_simulation()
