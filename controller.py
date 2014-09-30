import pygame
from pygame import joystick

def getAxes():
	pygame.event.pump()
	axes = []
	for i in range(0, js.get_numaxes()):
		axes.append(js.get_axis(i))
	return axes

def getNumAxes():
	return js.get_numaxes()

pygame.init()
js = joystick.Joystick(0)
js.init()
print 'Joystick %s initialized at ID ' % js.get_name(), js.get_id()
#print 'ID: %s' % js.get_id()
print 'Number of axes: %d' % js.get_numaxes()
