from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16

JOYSTICK_REF_NAME = 'joystick-ref-chan'

class JOYSTICK_REF(Structure):
	_pack_ = 1
	_fields_ = [('axis', c_double * 6)]
