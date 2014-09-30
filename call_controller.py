import controller
import joystick_include as ji
import ach
import sys
import time
import numpy as np
from ctypes import *

c = ach.Channel(ji.JOYSTICK_REF_NAME)
joystick = ji.JOYSTICK_REF()

while(1):
	time.sleep(.1) #figure out a decent polling frequency
	axis = controller.getAxes()
#	for i in range(0, len(axis)):
	for i in range(0, 6):
		if i < controller.getNumAxes():
			print 'Axis', i, ': ', axis[i]
			joystick.axis[i] = axis[i]
		else:
			print 'Axis', i, ': ', 0.0
			joystick.axis[i] = 0.0
#	joystick.axis[0] = axes[0]
#	joystick.axis[1] = axes[1]
#	joystick.axis[2] = axes[2]
#	joystick.axis[3] = axes[3]
	c.put(joystick)
