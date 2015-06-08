all:
	./drl-optimize.py arduino-shield.drl > arduino-shield.opt.drl
	pcb2gcode
