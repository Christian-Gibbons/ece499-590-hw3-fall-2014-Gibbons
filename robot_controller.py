#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro <dan (at) danLofaro (dot) com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */
import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import actuator_sim as ser

import joystick_include as ji
from joystick_include import JOYSTICK_REF_NAME
from robot_simple_move import simpleMove
from robot_intelligent_move import intelligentMove

dd = diff_drive
ref = dd.H_REF()
tim = dd.H_TIME()

jstate = ji.JOYSTICK_REF()


ROBOT_DIFF_DRIVE_CHAN   = 'robot-diff-drive'
ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
# CV setup 
r = ach.Channel(ROBOT_DIFF_DRIVE_CHAN)
r.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
j = ach.Channel(JOYSTICK_REF_NAME)
j.flush()

i=0

defaultControlMode = "idcs"
if(len(sys.argv) > 1):
	controlMode = sys.argv[1]
	if(sys.argv[1] != "idcs" and sys.argv[1] != "simple"):
		print sys.argv[1], " not recognized as control mode.  Using default:"
		controlMode = defaultControlMode
else:
	print "No control mode selected (\"idcs\" or \"simple\").  Using default:"
	controlMode = defaultControlMode


if(controlMode == "simple"): #simple control system; axis 1 controls left wheel, axis 3 controls right wheel
	print "Simple Control System.  Axis 1 controls left wheel and axis 3 controls right wheel."
elif(controlMode == "idcs"): #intelligent drive control system; uses axes 0 and 1 to
	print "Intelligent Drive Control System.  Axis 0 acts as rudder and axis 1 acts as throttle."
else: #should be unreachable
	print "Invalid control mode."

print '======================================'
print '============= Robot-View ============='
print '========== Daniel M. Lofaro =========='
print '========= dan@danLofaro.com =========='
print '======================================'
ref.ref[0] = 0
ref.ref[1] = 0

updatePeriod = 0.05
while True:
	[status, framesize] = t.get(tim, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		pass
		#print 'Sim Time = ', tim.sim[0]
	else:
		raise ach.AchException( v.result_string(status) )
	timeStart = tim.sim[0]
	
	#Main loop

	#grab axis values from joystick channel
	[statusj, framesizej] = j.get(jstate, wait=False, last=False)
	#for i in range(0, 6):
		#print 'Axis ', i, ' = ', jstate.axis[i]
	if(controlMode == "simple"):
		buff = simpleMove(jstate)
	elif(controlMode == "idcs"):
		buff = intelligentMove(jstate)
	ref = ser.serial_sim(r, ref, buff[0])
	ref = ser.serial_sim(r, ref, buff[1])
	

	#sleep until the update period as passed
	[status, framesize] = t.get(tim, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		pass
		#print 'Sim Time = ', tim.sim[0]
	else:
		raise ach.AchException( v.result_string(status) )
#	time.sleep(updatePeriod - (tim.sim[0]- timeStart) )
	time.sleep(updatePeriod)


