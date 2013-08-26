<b>NDS - Networked Dyanmic Systems</b>

This python library is used to model and simulate networks represented by graphs.

In it's current form it served me as mostly an excercise as well as a learning tool for Python and math concepts such as graph-theory, control-systems and linear algebra.

The networks are composed of graphs, where each graph itself is composed of

-- Nodes and 

-- Edges.

You can follow the Demo.py file to see how it works.
You can keep the network-graph description in a separate text file or in the program itself. The graph format should be as follows:

nodes = "#nodeId(Xpos,Ypos)-..."

edges = "#edgeId(#nodeId<>#nodeId)-..."

For the edges you can specify either '<' / '>' / '<>' for connectivity.

Also please notice it is possible to start a <b>Process</b> for a graph where a control law will be activated for the nodes based on the graph's connectivity. The control law is based on consensus.

<b>NDSTurtle - Simple visualization of the graph</b>

This little module takes in a Graph object and outputs the graph to the screen. This is very simple and primitive, and the worst is it's very inefficient.
I had a much better implementation using tkinter directly, not through turtle, but I'm still trying to find it.
