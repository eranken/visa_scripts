import pyvisa 
rm = pyvisa.ResourceManager('@py')
print(rm)
res=rm.list_resources('?*')
print(res)

power = rm.open_resource('USB0::1510::8736::9010039::0::INSTR')

print(power.query('*IDN?'))

power.write('INST:SEL CH1')
power.write('CHANNEL:OUTPUT ON')
power.write('INST:SEL CH2')
power.write('CHANNEL:OUTPUT ON')

power.write('APPLY CH1,4V,1A')
power.write('APPLY CH2,1.5V,1A')


#print(power.write('DISP:TEXT?'))
print(power.query('MEAS:VOLT? ALL'))
#print(power.write('FETC:VOLT? ALL'))
