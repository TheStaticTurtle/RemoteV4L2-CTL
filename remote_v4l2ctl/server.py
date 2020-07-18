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

	def register_external_int_command(self, callback,name, min=0, max=100):
		self.driver.controls.append(utils.V4L2_Control(
			"user",
			name,
			"0x0",
			"custom",
			min=min,
			max=max,
			step=-99,
			default=0,
			value=0,
			flags="none",
			callback = callback
		))
		setattr(self, "set_" + name, self.driver.controls[-1].change_value)

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
					if data == b'get_capabilities':
						cap = self.driver.get_capbilities_as_json()
						self.client_socket.send(bytearray(cap, 'utf-8'))
					if b'value_set' in data:
						_, what, value = data.decode("utf-8").split("=")
						if self.driver.has_capability(what):
							fn = eval("self.driver.set_"+what)
							resp = str(fn(value))
							self.client_socket.send(bytearray(resp, 'utf-8'))

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
