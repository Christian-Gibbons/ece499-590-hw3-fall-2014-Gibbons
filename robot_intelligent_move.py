from robot_command import createCommandPacket
from joystick_include import JOYSTICK_REF_NAME
from params import multiplyVelocity

def intelligentMove(jstate):
	leftWheel = 0x01
	rightWheel = 0x00
	angle = jstate.axis[0] #negative number turns left, positive turns right
	throttle = -1.0 * jstate.axis[1] #Up on joystick gives -1, so make up positive
	fullSpeedAhead = [0xFF, 0x07]
	

	#start with digital test
	leftBuff = createCommandPacket(leftWheel, 4, 0x20, [0,0])
	rightBuff = createCommandPacket(rightWheel, 4, 0x20, [0,0])
#	if(angle == 0.0):
#		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
#		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
#	elif(angle < -0.9):
#		if(throttle > 0.9):
#			leftBuff = createCommandPacket(rightWheel, 4, 0x20, [0,0])
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, fullSpeedAhead)
#		elif(throttle == 0.0):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0))
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, fullSpeedAhead)
#		elif(throttle < -0.9):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, [0,0])
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0))
#	elif(angle > 0.9):
#		if(throttle > 0.9):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, fullSpeedAhead)
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, [0,0])
#		if(throttle == 0.0):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, fullSpeedAhead)
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0))
#		if(throttle < -0.9):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0))
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, [0,0])
#	else:
#		leftBuff = createCommandPacket(leftWheel, 4, 0x20, [0,0])
#		rightBuff = createCommandPacket(rightWheel, 4, 0x20, [0,0])

	#separate into quadrants
	#quadrant 1, left wheel moves with the throttle, right wheel moves at throttle-angle
	if((throttle > 0.0) and (angle > 0.0)):
		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle-angle)))
	#quadrant 2, right wheel moves with throttle, left wheel moves at throttle + angle
	elif((throttle > 0.0) and (angle < 0.0)):
		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle+angle)))
		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
	#quadrant 3, 
	elif((throttle < 0.0) and (angle < 0.0)):
		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle+angle)))
		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0*throttle))
	#quadrant 4
	elif((throttle < 0.0) and (angle > 0.0)):
		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0*throttle))
		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle-angle)))

	#x-axis
	elif(angle == 0.0):
		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
	#y-axis
	elif(throttle == 0.0):
		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, angle))
		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0*angle))
		
	#quadrant 3, 
#	elif((throttle < 0.0) and (angle < 0.0)):
#		if(throttle > angle):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (angle-throttle)))
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (2.0*throttle-1.0*angle)))
#		else:	
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle-angle)))
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0*throttle))
#	#quadrant 4
#	elif((throttle < 0.0) and (angle > 0.0)):
#		if(fabs(throttle) < angle):
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (angle + 2.0*throttle)))
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle-angle)))
#		else:
#			leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
#			rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle+angle)))


	#quadrant 3, 
#	elif((throttle < 0.0) and (angle < 0.0)):
#		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0*throttle))
#		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle-angle)))
#	#quadrant 4
#	elif((throttle < 0.0) and (angle > 0.0)):
#		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, (throttle+angle)))
#		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, -1.0*throttle))
#	#x-axis
#	elif(angle == 0.0):
#		leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
#		rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, throttle))
	
	buff = []
	buff.append(leftBuff)
	buff.append(rightBuff)
	return buff
