import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from D_Functions import dec_to_float32

client = ModbusClient(method = 'rtu' , port = 'COM17' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)
connection = client.connect()

response = client.read_input_registers(5097,2,unit=1)
SOC=dec_to_float32(response.registers[0], response.registers[1])
print SOC

response = client.read_input_registers(5003,2,unit=1)
#print response.registers[0]
#print response.registers[1]
PD=int(response.registers[1])
print PD

response = client.read_input_registers(5053,2,unit=1)
Pac_Grid=dec_to_float32(response.registers[0], response.registers[1])
print Pac_Grid

response = client.read_input_registers(5005,2,unit=1)
Vdc=dec_to_float32(response.registers[0], response.registers[1])
print Vdc

response = client.read_input_registers(5021,2,unit=1)
Iac_Ext=dec_to_float32(response.registers[0], response.registers[1])
print Iac_Ext

response = client.read_input_registers(5013,2,unit=1)
Vac_Out=dec_to_float32(response.registers[0], response.registers[1])
print Vac_Out