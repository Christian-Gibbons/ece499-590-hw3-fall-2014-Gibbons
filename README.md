Project written by Christian Gibbons

This contains the files created or changed to control the diff drive robot with an HID gamepad

Changed files:
	robot-view - added the channel to communicate with the process gathering the gamepad inputs

Created files:
	controller.py - initializes pygame and includes function to grab joystick axis information
	call_controller.py - uses controller.py to poll HID gamepad for axis information and pushes it to the channel
	joystick_include.py - contains structure and channel information
	robot_controller.py - takes axis information from channel and processes it to create servo signals to send to the diff drive channel
	robot_simple_move.py - Simple movement algorithm moving the wheels proportionally to the offset of Axis 1 and Axis 3 (should be the y-axis of the left and right analog sticks on a gamepad)
	robot_intelligent_move.py - Intelligent Drive Control System to make control more intuitive.  Uses Axis 0 to turn and Axis 1 to move.  Should act much like Rudder and Throttle, or the so-called "Tank Controls" as seen in Resident Evil 1.
	params.py - contains function for multiplying the velocity parameter of the diff drive instruction by a float; useful for proportional movement
	robot_command.py - contains function to create a command packet
	robot_checksum.py - contains function to create a checksum for a command packet


**Instructions for use**
Dependencies:
	This project requires the pygame library.  To install, from terminal, enter "apt-get install python-pygame"

Running program:
	First, make sure to start the diff drive robot through robot-view, which will set up the channel.
		"./robot-view server"
	
	Then run the robot_control program that will read the joystick channel and send to the diff_drive channel.  Here is when you will select your control mode.  Either pass in "simple" or "idcs" as the first argument.  Passing in no control system argument will default to the Intelligent Drive Control System.
		"python robot_control.py [control system]"
	
	And then to send the joystick axis information to the joystick channel for the robot_control to read, run call_controller.
		"python call_controller.py"
