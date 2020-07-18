import tkinter as tk
import logging
import remote_v4l2ctl
import time

logging.basicConfig(format='[%(asctime)s] [%(name)s]  [%(levelname)s] %(message)s', level=logging.DEBUG)
logging.warning('This is a Warning')

client = remote_v4l2ctl.client.ControlClient(host="192.168.2.50")

root = tk.Tk()

def value_change(what,value):
	fn = eval("client.set_"+what+"")
	fn(value)
	print(what+" = "+str(value))

y = 0
x = 0
vars = []
for control in client.remote_driver.controls:

		l = tk.Label(text=control.name, relief=tk.RIDGE)
		l.grid(row=y, column=x)


		if(control.type=="bool"):
			vars.append(tk.IntVar())
			fn = eval("lambda: value_change(\""+control.name+"\", vars["+str(len(vars)-1)+"].get())")
			s = tk.Checkbutton(relief=tk.RIDGE, command=fn, variable=vars[-1])
			vars[-1].set(control.value)
			s.grid(row=y, column=x+1)

		else:

			fn = eval("lambda value: value_change(\""+control.name+"\", value)")
			s = tk.Scale(from_= (0 if control.min == -99 else control.min) , relief=tk.RIDGE, to=(1 if control.max == -99 else control.max), orient=tk.HORIZONTAL, length=700, command=fn)
			s.set(control.value)
			s.grid(row=y, column=x+1)

		y+=1
		if(y> len(client.remote_driver.controls)/2):
			y=0
			x+=2

tk.mainloop()