import json
import logging
import socket
from . import utils

logger = logging.getLogger(__name__)


class ControlClient:
	"""docstring for ControlClient"""

	def __init__(self, host="127.0.0.1", port=5665):
		super(ControlClient, self).__init__()
		self.host = host
		self.port = port
		self.socket = None

		self.remote_driver = utils.V4L2_CTL_Remote()
		if self.connect():
			self.load_utils()

	def _wait_for_data(self, size):
		data = ""
		while not data:
			data = self.socket.recv(8162)
		return data

	def send_value_set(self, what, value):
		if self.socket is not None:
			self.socket.send(bytearray("value_set="+what+"="+str(value),"utf-8"))
			resp = self._wait_for_data(1024)
			return 0 if resp == "OK" else -1
		return -1

	def load_utils(self):
		if self.socket is not None:
			self.socket.send(b"get_capabilities")
			caps = self._wait_for_data(8162)
			self.remote_driver.load_controls(json.loads(caps))

			for control in self.remote_driver.controls:
				control.setServer(self)
				setattr(self, "set_" + control.name, control.change_value )

	def connect(self):
		if self.socket is None:
			logger.info("Connecting to server")
			try:
				self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.socket.connect((self.host, self.port))
				logger.info("Connected.")
				return True
			except Exception as e:
				logger.error("Failed to connect: " + str(e))
		else:
			logger.warning("Trying to connect while already connected")
		return False
