import pyvisa 
rm = pyvisa.ResourceManager('@py')
print(rm)
res=rm.list_resources('?*')
print(res)

scope = rm.open_resource('USB0::2733::279::026508776::0::INSTR')

#funcgen.read_termination = '\n'
#funcgen.write_termination = '\n'

# print identification
print(scope.query('*IDN?'))

#reset
#scope.write('*RST')

# sets horizontal scale for all channels 
# range 2E-9 to 50, default unit s/div
#scope.write(f"TIM:SCAL  50E-9")

# Defines horizontal trigger position , default unit = s
#scope.write(f"TIM:POS 0")

ch = 1
# sets status of channel ch [ON/OFF]
#scope.write(f"CHAN{ch}:STAT ON")

# sets the vertical scale for channel ch
# scale value in V/div , range 1E-3 to 10
scope.write(f"CHAN{ch}:SCAL 0.2")

# sets vertical position of ch in divisions
#scope.write(f"CHAN{ch}:POS 0")

#OFFSET
#scope.write(f"CHAN{ch}:OFFS  0")

# Sets trigger level in V, 1-4 are channels , 5 is external trigger
#scope.write(f"TRIG:A:LEV{ch} -0.02")

#Sets source for trigger A |use EXT instead of CH{ch} for external trigg
#scope.write(f"*ESD?")
#scope.write(f"SYST:ERR:ALL?")
#scope.write(f"SYST:ERR:NEXT?")
#scope.write(f"*CLS?")
#scope.write(f"TRIG:A:MODE AUTO")
#.write(f"TRIG:A:MODE NORMal")
#scope.write(f"SYST:ERR:ALL?")
#scope.write(f"CHAN{ch}:SCAL?")
#scope.write(f"TRIG:A:SOUR CH2")
#scope.write(f"TRIG:A:RISetime:SLOPe NEGative")
#scope.write(f"SYST:ERR:NEXT?")
