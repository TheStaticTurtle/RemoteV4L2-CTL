from remote_v4l2ctl import utils
import logging 
import time

logging.basicConfig(format='[%(asctime)s] [%(name)s]  [%(levelname)s] %(message)s',level=logging.DEBUG )
logging.warning('This is a Warning')

interpreter = utils.V4L2_CTL()

for i in interpreter.controls:
    print(i)

#while True:
#	for i in range(40,60):
#		interpreter.set_brightness(i)
#		time.sleep(.1)
while True:
	for i in range(0,10):
		interpreter.set_color_effects(i)
		time.sleep(1)
#print(interpreter.list_controls())
