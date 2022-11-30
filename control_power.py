import pyvisa 
import readline

help_dict = {
	"on [0]":"turn on channel [0]",
	"off [0]":"turn off channel [0]",
	"set [0] [1] [2]":"set channel [0] to apply [1](V) and [2](A)",
	"status":"print status of channel outputs",
	"query [...]":"send query [...] directly to machine, print result",
	"write [...]":"write [...] directly to machine",
	"h": "print this dict",
	"q": "turn off outputs and quit program"
}

def confirm(msg):
	print(msg)
	choice = input("[y/n] \n>>>").lower()
	if choice in ["yes","y"]:
		return True
	else: 
		print("ok, not doing it")
		return False
	
machine_commands = ["on","off","set","status","q","units", "query","write"]

def voltage_off():		
	power.write("APPLY CH1,0,1")
	power.write("APPLY CH2,0,1")
	power.write("INST:SEL CH1")
	power.write("CHANNEL:OUTPUT OFF")
	power.write("INST:SEL CH2")
	power.write("CHANNEL:OUTPUT OFF")

def machine_command(cmd_list):
	base_cmd = cmd_list[0]
	
	if base_cmd == "on":
		chan = cmd_list[1]
		chan=chan.replace("CH","")
		
		power.write(f"INST:SEL CH{chan}")
		
		volt_level= power.query(f"VOLT?").replace("\n","")
		curr_level= power.query(f"CURR?").replace("\n","")

		msg = f"confirm turn on channel {chan} with potential {volt_level}V and current {curr_level}A ?"
		if not confirm(msg): 
			return
		
		power.write("CHANNEL:OUTPUT ON")
		
	elif base_cmd == "off":
		chan = cmd_list[1]
		chan=chan.replace("CH","")
		
		power.write(f"INST:SEL CH{chan}")
		power.write("CHANNEL:OUTPUT OFF")
		
	elif base_cmd == "set":
		chan      = cmd_list[1]
		potential = cmd_list[2]
		current   = cmd_list[3] if len(cmd_list)>3 else 0.5
		
		if not "V" in potential: potential+="V"
		if not "A" in current: current+="A"
		
		msg = f"confirm set channel {chan} with potential {potential} and current {current} ?"
		if not confirm(msg): 
			return
		
		chan=chan.replace("CH","")
		power.write(f"APPLY CH{chan},{potential},{current}")
	
	elif base_cmd == "status":
		print("Voltages: "+power.query("MEAS:VOLT? ALL"))
		print("Currents: "+power.query("MEAS:CURR? ALL"))
		print("Power   : "+power.query("MEAS:POW? ALL"))
		return
	
	elif base_cmd == "query":
		cmd = " ".join(cmd_list[1:])
		try: print("query result:\n",power.query(cmd))
		except: print("oops, query did not work")
		return
	
	elif base_cmd == "write":
		cmd = " ".join(cmd_list[1:])
		try: power.write(cmd)
		except: print("oops, write command did not work")

		
	if base_cmd == "q":
		print("powering down")
		voltage_off()
		
	print("command sent. current status: \n")
	print("Voltages: "+power.query("MEAS:VOLT? ALL"))
	print("Currents: "+power.query("MEAS:CURR? ALL"))
	print("Power   : "+power.query("MEAS:POW? ALL"))
	
### MAIN CODE

rm = pyvisa.ResourceManager("@py")
power = rm.open_resource("USB0::1510::8736::9010039::0::INSTR")
connection_test = power.query('*IDN?')
print("Connection Test: \n\n", connection_test )

voltage_off()

### in case of connection failure, try:
#res=rm.list_resources("?*")
#print("Resource List:\n",res)

#print("query volts?",power.query("SOUR:VOLT:LEV? 1"))

while True:
	print("\n")
	cmd = input(">>>")
	
	cmd_args = cmd.split(" ")
	base_cmd = cmd_args[0]
		
	if cmd in ["help", "h"]:
		print("\n")
		for k,v in help_dict.items():
			print(f"{k:20} : {v}")
			
	elif base_cmd in machine_commands:
		try: machine_command(cmd_args)
		except: print("invalid command format? ")
	else: print("command not recognized, try \'h\' for help")
	
	if base_cmd=="q":
		break

