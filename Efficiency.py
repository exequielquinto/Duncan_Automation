import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from D_Functions import float32_to_msb, float32_to_lsb, pac_set
import numpy as np

client = ModbusClient(method = 'rtu' , port = 'COM1' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
#client = ModbusClient('127.0.0.1', 502)    #MODBUS TCP/IP

connection = client.connect()
#print(connection)

#For load sequence
bi_time=600  #5minsBurn In time in seconds
capture_time=120   # 2mins //time in seconds for each successive eff capture
#Discharge and Charge Eff
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
#load=(3000,2500,2000,1500,1400,1300,1200,1100,1000,900,800,700,600,500,250,0,-3000,-2500,-2000,-1500,-1400,-1300,-1200,-1100,-1000,-900,-800,-700,-600,-500,-250,0)

#steps=(0,1,2,3,4,5,6,7,8,9,10)
#load=(3000,2700,2400,2100,1800,1500,1200,900,600,300,0)
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
#load=(3000,2700,2400,2100,1800,1500,1400,1300,1200,1100,1000,900,800,700,600,500,400,300,200,100,0)

#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45)
#load=(3000,2700,2400,2100,2000,1800,1500,1400,1300,1200,1100,1000,900,800,700,600,500,400,300,200,100,50,0,-3000,-2700,-2400,-2100,-2000,-1800,-1500,-1400,-1300,-1200,-1100,-1000,-900,-800,-700,-600,-500,-400,-300,-200,-100,-50,0)
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
load=(3000,2700,2400,2100,2000,1800,1500,1200,1000,900,600,300,0,-3000,-2700,-2400,-2100,-2000,-1800,-1500,-1200,-1000,-900,-600,-300,0)

steps=np.arange(0,len(load))
print steps
print load

for step in steps:
    #pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
    #time.sleep(2)
    #pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
    #time.sleep(2)
    #pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
    #time.sleep(2)
    #pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
    
    if load[step]==3000 or load[step]==-3000:
        test_time=bi_time
        print step
        print ('burn in... time now is ' + time.ctime())
    else:
        test_time=capture_time
        print step
        print ('capturing... time now is ' + time.ctime())
    
    time2=time.time()
    while (time.time()-time2) < test_time:
        pac_set(float32_to_msb(load[step]),float32_to_lsb(load[step]),client)
        time.sleep(5)  # send Pac setpoint repeat
        #print('testing2')
    #time.sleep(test_time)
    print('measure')

pac_set(float32_to_msb(0),float32_to_lsb(0),client)               
print('finished')
