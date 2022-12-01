import pyvisa 
import readline
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true")
args = parser.parse_args()


help_dict = {
	"channels are" : "0-4, 5=external trigger",
	"on [ch]" : "turn on channel [ch]",
	"off [ch]" : "turn off channel [ch]",
	"tscale [t]": "set time scale for all channels to [t](s)",
	"scale [ch] [y]":"set channel [ch] scale to [y](V)",
	"tpos [t]": "set time position for all channels to [t](div)",
	"pos [ch] [y]" : "set the y position of channel [ch] to [y](div)",
	"offset [ch] [t]": "set offset of channel [ch] to [t]", 
	"trigsource [ch]": "set trigger source to channel [ch]",
	"triglevel [ch] [lv]": "set trigger threshold for channel [ch] level to [lv](V)",
	"trigslope [slope]": "set trigger [slope] to 'POS' or 'NEG'",
	"trigmode [mode]": "set trigger [mode] to 'AUTO' or 'NORM'",
	"trigtype [type]": "set trigger [type] to 'EDGE', 'WIDTH', 'BUS', ...",
	"trigcoupling [mode]": "set the trig coupling [mode] to 'AC' or 'DC'",
	"reset" : "reset the scope to default settings",
	"query [CMD]": "send a query 'CMD' directly to the machine, e.g. '*IDN?'",
	"write [CMD]": "send a write command 'CMD' directly to the machine, e.g. 'CHAN1:STAT ON'",
	"h": "print this dict",
	"q": "quit program",
}
	
machine_commands = ["query","write", "scale", "tscale","trigslope","tpos","pos","reset","offset", "trigsource","trigmode","triglevel","trigcoupling", "on","off"]

init_commands = ["trigmode AUTO","trigtype SLOPE","trigslope NEG","trigcoupling DC"]

def confirm(msg):
	print(msg)
	choice = input("[y/n] \n>>>").lower()
	if choice in ["yes","y"]:
		return True
	else: 
		print("ok, not doing it")
		return False

def machine_command(cmd):
	cmd_list = cmd.split(" ")
	base_cmd = cmd_list[0]
	
	if base_cmd == "on":
		chan  = cmd_list[1]	
		chan=chan.replace("CH","")
		scope.write(f"CHAN{chan}:STAT ON")
		
	if base_cmd == "off":
		chan  = cmd_list[1]	
		chan=chan.replace("CH","")
		scope.write(f"CHAN{chan}:STAT OFF")

	if base_cmd == "offset":
		chan  = cmd_list[1]	
		offset = cmd_list[2]
		chan=chan.replace("CH","")
		scope.write(f"CHAN{chan}:OFFS {offset}")

	if base_cmd == "trigmode":
		mode = cmd_list[1]
		scope.write(f"TRIG:A:MODE {mode}")
		
	if base_cmd == "trigtype":
		mode = cmd_list[1]
		scope.write(f"TRIG:A:TYPE {mode}")

	if base_cmd == "trigslope":
		slp = cmd_list[1]
		scope.write(f"TRIG:A:EDGE:SLOPE {slp}")		

	if base_cmd == "trigcoupling":
		mode = cmd_list[1]
		scope.write(f"TRIGger:A:EDGE:COUPLING {mode}")	

	if base_cmd == "triglevel":
		chan  = cmd_list[1]	
		lev = cmd_list[2]
		chan=chan.replace("CH","")
		scope.write(f"TRIG:A:LEV{chan} {lev}")

	if base_cmd == "trigsource":
		chan  = cmd_list[1]	
		chan=chan.replace("CH","")
		scope.write(f"TRIG:A:SOUR{chan}")
		
		

	if base_cmd == "tscale":
		scale = cmd_list[1].lower()
		
		if not "s" in scale: scale+="s"
		
		print(f"setting time scale to {scale} ")
		scope.write(f"TIM:SCAL {scale}")
		
	if base_cmd == "tpos":
		pos = cmd_list[1].lower()
		
		if not "s" in scale: pos+="s"
		
		print(f"setting time position to {pos} ")
		scope.write(f"TIM:POS {pos}")

	if base_cmd == "pos":
		chan = cmd_list[1]
		pos = cmd_list[2]
		
		print(f"setting chan {chan} vertical position to {pos} ")
		scope.write(f"CHAN{chan}:POS {pos}")

	if base_cmd == "scale":
		chan  = cmd_list[1]
		scale = cmd_list[2]
		
		scale=scale.replace("v","V")
		if not "V" in scale: scale+="V"
		
		print(f"setting channel {chan} with scale {scale} ")
		
		chan=chan.replace("CH","")
		scope.write(f"CHAN{chan}:SCAL {scale}")
		
	if base_cmd == "query":
		cmd = " ".join(cmd_list[1:])
		try: print("query result:\n",scope.query(cmd))
		except: print("oops, query did not work")
		return
	
	if base_cmd == "write":
		cmd = " ".join(cmd_list[1:])
		try: scope.write(cmd)
		except: print("oops, write command did not work")
		
	if base_cmd == "reset":
		msg = "reset the scope?"
		if not confirm(msg):
			return
		scope.write(f"*RST")
	
### MAIN CODE

rmstring = "@py"
inst_address = "USB0::2733::279::026508776::0::INSTR"
if args.debug:
	rmstring = "@sim"
	inst_address = "ASRL1::INSTR"
	print("***debug mode, simulated device***")
rm = pyvisa.ResourceManager(rmstring)
rm.list_resources()
scope = rm.open_resource(inst_address)
connection_test = scope.query('*IDN?')
print("Connection Test: \n\n", connection_test )

### in case of connection failure, try:
#res=rm.list_resources("?*")
#print("Resource List:\n",res)

for cmd in init_commands:
	print("initializing with command :"+cmd)
	try: machine_command(cmd)
	except: print("ERROR: invalid initial command? ")	

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
		try: machine_command(cmd)
		except: print("invalid command format? ")
	elif base_cmd=="q":
		break
	else: print("command not recognized, try \'h\' for help")
	

