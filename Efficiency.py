import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from D_Functions import float32_to_msb, float32_to_lsb

client = ModbusClient(method = 'rtu' , port = 'COM9' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
#client = ModbusClient('127.0.0.1', 502)    #MODBUS TCP/IP

connection = client.connect()
print(connection)

#For load sequence
bi_time=600  #15minsBurn In time in seconds
capture_time=30   # 3mins //time in seconds for each successive eff capture
#Discharge and Charge Eff
steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
load=(3000,2500,2000,1500,1400,1300,1200,1100,1000,900,800,700,600,500,250,0,-3000,-2500,-2000,-1500,-1400,-1300,-1200,-1100,-1000,-900,-800,-700,-600,-500,-250,0)

#steps=(0,1,2,3,4,5,6)
#load=(-3000,-2500,-2000,-1500,-1000,-500,0)


print steps
print load

#Funtions
def pac_set():
    try:
        client.write_register(5054, float32_to_msb(load[step]))
        client.write_register(5055, float32_to_lsb(load[step]))
    except:
        try:
            print('pac set error1')
            client.write_register(5054, float32_to_msb(load[step]))
            client.write_register(5055, float32_to_lsb(load[step]))
        except:
            print('pac set error2')
            client.write_register(5054, float32_to_msb(load[step]))
            client.write_register(5055, float32_to_lsb(load[step]))
    
def min_load():
    try:
        client.write_register(5054, float32_to_msb(0))
        client.write_register(5055, float32_to_lsb(0))
    except:
        try:
            print('pac set error1')
            client.write_register(5054, float32_to_msb(0))
            client.write_register(5055, float32_to_lsb(0))
        except:
            print('pac set error2')
            client.write_register(5054, float32_to_msb(0))
            client.write_register(5055, float32_to_lsb(0))

for step in steps:
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
        pac_set()
        time.sleep(3)
        #print('testing2')

    print('measure')

min_load()                
print('finished')