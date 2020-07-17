import logging
import socket

logger = logging.getLogger(__name__)


class ControlClient:
	"""docstring for ControlClient"""

	def __init__(self, host="127.0.0.1", port=5665):
		super(ControlClient, self).__init__()
		self.host = host
		self.port = port
		self.socket = None

		if self.connect():
			self.get_capabilities()


	def get_capabilities(self):
		if self.socket is not None:
			self.socket.write("get_capabilities")

	def connect(self):
		if self.socket is None:
			logger.info("Connecting to server")
			try:
				self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.socket.connect((self.host, self.port))
				logger.info("Connected.")
			except Exception as e:
				logger.error("Failed to connect: "+str(e))
		else:
			logger.warning("Trying to connect while already connected")
