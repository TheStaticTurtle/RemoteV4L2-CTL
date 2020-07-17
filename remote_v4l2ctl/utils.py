import subprocess
import logging

logger = logging.getLogger(__name__)

class V4L2_Control():
	"""docstring for V4L2_CTL"""
	def __init__(self, control_group, name, addr, type, min=-99, max=-99, step=-99, default=-99, value=-99, flags="none", access="local", device="/dev/video0"):
		super(V4L2_Control, self).__init__()
		self.control_group = control_group

		self.name = name
		self.addr = addr
		self.type = type
		self.min = min
		self.max = max
		self.step = step
		self.default = default
		self.value = value
		self.flags = flags

		self.access = access
		self.device = device

	def change_value(self, value, server=None):
		if(self.access == "local"):
			try:
				value = int(value)
			except Exception as e:
				logger.error("change_value: Invalid input -> "+str(e))
				return -1

			if value < self.min:
				logger.error("change_value: Value too little")
				return -1

			if value > self.max:
				logger.error("change_value: Value too big")
				return -1

			if self.step != 99 and value % self.step != 0:
				logger.error("change_value: Invalid step number (Steps per "+str(self.step)+")")
				return -1
			
			logger.info("Executing: " + ' '.join(['v4l2-ctl', '-d', self.device, '--set-ctrl='+self.name+'='+str(value)]))
			output = subprocess.check_output(['v4l2-ctl', '-d', self.device, '--set-ctrl='+self.name+'='+str(value)]).decode("utf-8")
		else:
			if server == None:
				pass 

	def __repr__(self):
		return str(self)

	def __str__(self):
		out = "V4L2_Control() -> " + self.name + " " + self.addr + " (" + self.type + ")  :  "
		out += "min="+str(self.min)+" " if self.min != -99 else ""
		out += "max="+str(self.max)+" " if self.max != -99 else ""
		out += "step="+str(self.step)+" " if self.step != -99 else ""
		out += "default="+str(self.default)+" " if self.default != -99 else ""
		out += "value="+str(self.value)+" " if self.value != -99 else ""
		out += "flags="+self.flags+" " if self.flags != "none" else ""
		return out

class V4L2_CTL():
	"""docstring for V4L2_CTL"""
	def __init__(self, device="/dev/video0"):
		super(V4L2_CTL, self).__init__()
		self.device = device
		self.controls = self._list_controls()

		for control in self.controls:
			setattr(self, "set_"+control.name , control.change_value)

	def _list_controls(self):
		controls = []
		logger.info("Executing: " + ' '.join(['v4l2-ctl', '-d', self.device, '-l']))
		output = subprocess.check_output(['v4l2-ctl', '-d', self.device, '-l']).decode("utf-8") #TODO: Check if the output is valid
		raw_ctrls = [x for x in output.split('\n') if x] #TODO: Same
		
		last_control_group = "unknown"
		for raw_ctrl in raw_ctrls:
			if(raw_ctrl[0] != ' '):
				last_control_group = ('_'.join(raw_ctrl.split(" ")[:-1])).lower()
				logger.debug("Found new control group: " +last_control_group)
			else:
				#Remove double white spaces
				while "  " in raw_ctrl:
					raw_ctrl = raw_ctrl.replace("  "," ")

				raw_ctrl_what, raw_ctrl_values  = raw_ctrl.split(":")
				raw_ctrl_what = [x for x in raw_ctrl_what.split(' ') if x and x != ' ']

				values = {
					"min": -99,
					"max": -99,
					"step": -99,
					"default": -99,
					"value": -99,
					"flags": "none"
				}

				for name,value in [name_value_combo.split("=") for name_value_combo in raw_ctrl_values.split(" ") if "=" in name_value_combo]:
					values[name] = value

			
				
				ctrlr = V4L2_Control(
					last_control_group, 
					raw_ctrl_what[0],
					raw_ctrl_what[1],
					raw_ctrl_what[2].replace("(","").replace(")",""),
					min= int(values["min"]),
					max = int(values["max"]),
					step = int(values["step"]),
					default = int(values["default"]),
					value= int(values["value"]),
					flags= values["flags"],
					device= self.device
				)

				logger.debug("Added new control parameter" +str(ctrlr))
				controls.append(ctrlr)

		logger.info("Done searching for controls. "+str(len(controls))+" found.")
		return controls