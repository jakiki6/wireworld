from ww import *
import os, time

height, width = os.get_terminal_size().lines, os.get_terminal_size().columns
chars = [
	" ",
	"@",
	"*",
	"O"
]

def show():
	print("\x1b[H\x1b[2J\x1b[3J", end="")

	for y in range(0, height):
	    for x in range(0, width):
	        print(chars[get_at(x, y)], end="")

	    if y < (height - 1):
	        print()

while True:
	show()
	tick()
	time.sleep(0.1)
