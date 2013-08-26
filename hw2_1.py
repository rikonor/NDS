from NDS import *
import TurtleNDS
import re
import numpy as np
import sys

if len(sys.argv) > 1:
	f_name = sys.argv[1]
	f = open(f_name)
	nodeString = f.readline()
	edgeString = f.readline()

g = Graph()
g.add_node(nodeString)
g.add_edge(edgeString)

print g.print_graph()

p = Process()
p.set_graph(g)

c = TurtleNDS.Canvas()
for node in p.Graph.Nodes:
	c.add_turtle(node.Value['x'],node.Value['y'])

for i in range(0,200):
	p.Act()
	c.set_positions(p.Graph.extract_values())

print g.print_graph()