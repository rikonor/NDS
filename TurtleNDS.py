import turtle
import math
import random

class Turtle(object):

	def __init__(self):
		self.p = turtle.Turtle()
		self.p.speed(0)

	def setpos(self, x, y):
		self.p.penup()
		self.p.setpos(x,y)
		self.p.pendown()

	def move_to(self, x, y):
		self.p.setpos(x, y)

	def drawCircle(self, x, y, r=1):
		n = 6
		theta_d = 360/n
		theta_r = theta_d*math.pi/180
		l = 2*r*math.tan(theta_r/2)
		self.setpos(x-l/2,y-r)
		for i in range(0,n):
			self.p.forward(l)
			self.p.left(theta_d)

class Canvas(object):

	def __init__(self):
		self.Turtles = []
		self.ColorList = ['green','blue','black','orange','red','purple','pink','turquoise','yellow','gold']

	def add_turtle(self, x, y):
		t = Turtle()
		t.setpos(x, y)

		t.p.color(random.choice(self.ColorList))
		self.Turtles.append(t)

	def set_positions(self, l):
		for i in range(0,len(self.Turtles)):
			self.Turtles[i].move_to(l[i]['x'], l[i]['y'])


