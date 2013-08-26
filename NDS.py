#! /usr/bin/env python
import math
import numpy as np
import time
import re
import random
import time

class Process(object):

    def __init__(self):
        self.dt = 0.01

    def set_graph(self, grph):
        self.Graph = grph

    def Act(self):
        vals = []
        for node in self.Graph.Nodes:
            xd_val = 0
            yd_val = 0
            for e in node.inEdges:
                if e.a.i != node.i:
                    xd_val = xd_val + e.Weight*(e.a.Value['x'] - node.Value['x'])*self.dt
                    yd_val = yd_val + e.Weight*(e.a.Value['y'] - node.Value['y'])*self.dt
                if e.a.i == node.i:
                    xd_val = xd_val + e.Weight*(e.b.Value['x'] - node.Value['x'])*self.dt
                    yd_val = yd_val + e.Weight*(e.b.Value['y'] - node.Value['y'])*self.dt
            val = {'x':node.Value['x'] + xd_val, 'y':node.Value['y'] + yd_val}
            vals.append(val)
        self.Graph.set_nodes_values(vals)

class Graph(object):

    def __init__(self):
        self.Nodes = []
        self.Edges = []

    def add_node(self, node):
        if node.__class__.__name__ == Node.__name__:
            self.Nodes.append(node)
            return
        if type(node) == type(str()):
            nodePattern = re.compile('^(\d*)\((\d*),(\d*)\)$')
            # i(x,y)
            nodeList = node.split("-")
            for nStr in nodeList:
                n = nodePattern.search(nStr).groups()

                i = int(n[0])
                nVal = {'x':float(n[1]) ,'y':float(n[2])}
                self.add_node(Node(i,nVal))

    def remove_node(self,node):
        if node.__class__.__name__ == Node.__name__:
            to_del = []
            for edge in node.inEdges:
                to_del.append(edge)
            for edge in to_del:
                self.remove_edge(edge)
            to_del = []
            for edge in node.outEdges:
                to_del.append(edge)
            for edge in to_del:
                self.remove_edge(edge)
            if self.Nodes.count(node) == 1:
                self.Nodes.remove(node)
            return
        if type(node) == type(int()):
            self.remove_node(self.find_node(node))

    def remove_all_nodes(self):
        to_del = []
        for node in self.Nodes:
            to_del.append(node)
        for node in to_del:
            self.remove_node(node)

    def find_node(self,i):
        for node in self.Nodes:
            if node.i == i:
                return node

    def add_edge(self, edge):
        if edge.__class__.__name__ == Edge.__name__:
            self.Edges.append(edge)
            return
        if type(edge) == type(str()):
            edgePattern = re.compile('^(\d*)\((\d*)(<?)(>?)(\d*)\)(\d*).?(\d*)$')
            # i(a<>b)w -> (i,a,<,>,b,w,w)
            edgeList = edge.split("-")
            for eStr in edgeList:
                e = edgePattern.search(eStr).groups()
                
                i = int(e[0])
                a = self.find_node(int(e[1]))
                b = self.find_node(int(e[4]))
                if len(e[5])>0:
                    w = float( e[5]+'.'+e[6] )
                else:
                    w = 1
                
                if e[2]=='<' and e[3]=='>':
                    undirected = True
                if e[2]=='' and e[3]=='>':
                    undirected = False
                if e[2]=='<' and e[3]=='':
                    undirected = False
                    a = self.find_node(int(e[4]))
                    b = self.find_node(int(e[1]))

                self.add_edge(Edge(i,w,a,b,undirected))

    def remove_edge(self, edge):
        if edge.__class__.__name__ == Edge.__name__:
            if edge.a.inEdges.count(edge) == 1:
                edge.a.inEdges.remove(edge)
            if edge.a.outEdges.count(edge) == 1:
                edge.a.outEdges.remove(edge)
            if edge.b.inEdges.count(edge) == 1:
                edge.b.inEdges.remove(edge)
            if edge.b.outEdges.count(edge) == 1:
                edge.b.outEdges.remove(edge)
            if self.Edges.count(edge) == 1:
                self.Edges.remove(edge)
            return
        if type(edge) == type(int()):
            self.remove_edge(self.find_edge(edge))

    def remove_all_edges(self):
        to_del = []
        for edge in self.Edges:
            to_del.append(edge)
        for edge in to_del:
            self.remove_edge(edge)

    def replace_graph(self, edges):
        self.remove_all_edges()
        self.add_edge(edges)

    def find_edge(self,i):
        for edge in self.Edges:
            if edge.i == i:
                return edge

    def set_nodes_values(self, l):
        for i in range(0, len(l)):
            self.Nodes[i].Value = l[i]

    def print_nodes(self):
        print "Nodes:"
        for node in self.Nodes:
            print "#%s: %s" % (node.i, node.Value) 
    
    def extract_values(self):
        val = []
        for node in self.Nodes:
            val.append(node.Value)
        return val

    def print_edges(self):
        print "Edges:"
        for edge in self.Edges:
            if edge.undirected == False:
                print "#%s: (%s -> %s) (w=%s)" % (edge.i, edge.a.i, edge.b.i, edge.Weight)
            if edge.undirected == True:
                print "#%s: (%s <-> %s) (w=%s)" % (edge.i, edge.a.i, edge.b.i, edge.Weight)

    def print_graph(self):
        self.print_nodes()
        self.print_edges()

    def complete_graph(self, n):
        for i in range(n):
            v = {'x':100*math.cos(2*math.pi*i/n),'y':100*math.sin(2*math.pi*i/n)}
            self.add_node(Node(i,v))
        index = 0
        for i in range(n):
            for j in range(i,n):
                if i!=j:
                    e = str(index)+'('+str(i)+"<>"+str(j)+')'
                    self.add_edge(e)
                    index = index + 1

    def cycle_graph(self, n, undirected=True):
        for i in range(n):
            v = {'x':100*math.cos(2*math.pi*i/n),'y':100*math.sin(2*math.pi*i/n)}
            self.add_node(Node(i,v))
        index = 0
        for i in range(n):
            if undirected == True:
                e = str(index)+'('+str(i)+"<>"+str((i+1)%n)+')'
            else:
                e = str(index)+'('+str(i)+">"+str((i+1)%n)+')'
            self.add_edge(e)
            index = index + 1              

    def random_graph(self, n, undirected=True):
        for i in range(n):
            Px = -100+200*random.random()
            Py = -100+200*random.random()
            v = {'x':Px,'y':Py}
            self.add_node(Node(i,v))
        index = 0
        for i in range(n):
            for j in range(i,n):
                if i!=j:
                    if random.choice([True,False]):
                        e_undirected = random.choice([True, False])
                        if e_undirected == True or undirected == True:
                            e = str(index)+'('+str(i)+"<>"+str(j)+')'
                        else:
                            e = str(index)+'('+str(i)+">"+str(j)+')'
                        self.add_edge(e)
                        index = index + 1        

###################################################

class Node(object):

    def __init__(self, i, val):
        self.Value = val
        self.i = i
        self.inEdges = []
        self.outEdges = []

class Edge(object):

    def __init__(self, i, w, a, b, undirected):
        self.Weight = w
        self.i = i
        self.a = a
        self.b = b
        self.undirected = undirected

        self.a.outEdges.append(self)
        self.b.inEdges.append(self)

        if undirected == True:
            self.b.outEdges.append(self)
            self.a.inEdges.append(self)



################# Actual program #############

nodes = "1(0,0)-2(100,0)-3(110,150)-4(0,100)"
edges = "1(1<>2)-2(3>2)-3(4>1)"

g = Graph()
g.add_node(nodes)
g.add_edge(edges)
g.print_graph()