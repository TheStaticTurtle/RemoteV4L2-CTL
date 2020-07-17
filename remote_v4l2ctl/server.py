import logging
import socket
import time
from threading import Thread

from . import utils

logger = logging.getLogger(__name__)


class ControlServer:
	"""docstring for ControlServer"""

	def __init__(self, host="0.0.0.0", port=5665):
		super(ControlServer, self).__init__()

		self.host = host
		self.port = port

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((host, port))
		self.socket.listen(5)

		self.driver = utils.V4L2_CTL()
		self.remote_clients = []

	class RemoteClient(Thread):
		def __init__(self, client_socket, address, driver):
			Thread.__init__(self)
			self.client_socket = client_socket
			self.address = address
			self.driver = driver

		def run(self):
			while True:
				time.sleep(.05)
				data = self.client_socket.recv(1024)
				if data:
					print(data)
					if data == "get_capabilities":
						self.client_socket.write("ABCD")

	def accept_connexion(self, client_socket, address):
		clt = ControlServer.RemoteClient(
			client_socket,
			address,
			self.driver
		)
		self.remote_clients.append(clt)
		clt.start()

	def run(self, once=False):
		logger.info("Now listening for clients")
		if once:
			client_socket, address = self.socket.accept()
			self.accept_connexion(client_socket, address)
			logger.info("Accepted connexion from: " + str(address))
		else:
			while True:
				client_socket, address = self.socket.accept()
				self.accept_connexion(client_socket, address)
				logger.info("Accepted connexion from: " + str(address))
