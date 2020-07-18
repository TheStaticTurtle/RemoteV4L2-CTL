import remote_v4l2ctl
import logging
import time

logging.basicConfig(format='[%(asctime)s] [%(name)s]  [%(levelname)s] %(message)s', level=logging.DEBUG)
logging.warning('This is a Warning')

client = remote_v4l2ctl.client.ControlClient(host="192.168.2.50")

client.set_brightness(80)