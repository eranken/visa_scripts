import pyvisa 
rm = pyvisa.ResourceManager('@py')
print(rm)
res=rm.list_resources('?*')
print(res)
funcgen= rm.open_resource('USB0::2391::16648::MY51400361::0::INSTR')
funcgen.read_termination = '\n'
funcgen.write_termination = '\n'
print(funcgen.query('*IDN?'))

#reset
#funcgen.write('*RST')

#Apply a pulse on channel 1 with a frequency of 100Hz, 
#an amplitude of 1 V and an offset of -0.5V
#funcgen.write(':APPL1:PULS 100Hz, 1.0, -0.5')

# set pulse width of ch 1
funcgen.write(':FUNC1:PULS:WIDT 200 NS')
# set pulse delay of ch 1
#funcgen.write(':FUNC1:PULS:DEL 20 NS')
# invert the output of ch1
#funcgen.write(':OUTP1:POL INV')
#couple the output of ch 1 and ch 2
#funcgen.write(':TRAC:CHAN1 ON')

#set into triggered mode
#funcgen.write(':ARM:SOUR EXT')
