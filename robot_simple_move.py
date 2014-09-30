from robot_command import createCommandPacket
from joystick_include import JOYSTICK_REF_NAME
from params import multiplyVelocity

def simpleMove(jstate):
	leftWheel = 0x01
	rightWheel = 0x00
	leftAxis = -1.0 * jstate.axis[1] #Up on joystick give -1, so make up positive
	rightAxis = -1.0 * jstate.axis[3]
	fullSpeedAhead = [0xFF, 0x07]
#	fullReverse = [0xFF, 0x03]
	leftBuff = createCommandPacket(leftWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, leftAxis))
	rightBuff = createCommandPacket(rightWheel, 4, 0x20, multiplyVelocity(fullSpeedAhead, rightAxis))
	buff = []
	buff.append(leftBuff)
	buff.append(rightBuff)
	return buff
