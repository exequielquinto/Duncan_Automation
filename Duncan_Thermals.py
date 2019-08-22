import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from D_Functions import dec_to_float32

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL18::INSTR')
client = ModbusClient(method = 'rtu' , port = 'COM12' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)
connection = client.connect()
#print(connection)

#FUNTIONS

def measure():
    #Time
    temp['A_Time']=time.ctime()
    
    #Minutes
    temp['B_Mins']=round((time.time()-ref_time)/60)
    
    #Measure PD
    response = client.read_input_registers(5003,2,unit=1)
    #print response.registers[0]
    #print response.registers[1]
    PD=int(response.registers[1])
    temp['C_PD'] = PD
    
    #Measure SOC
    response = client.read_input_registers(5097,2,unit=1)
    SOC=dec_to_float32(response.registers[0], response.registers[1])
    temp['D_SOC'] = SOC
    
    #Measure Pac_Grid
    response = client.read_input_registers(5053,2,unit=1)
    Pac_Grid=dec_to_float32(response.registers[0], response.registers[1])
    temp['E_Pac_Grid'] = Pac_Grid
    
    #Measure Batt Vdc
    response = client.read_input_registers(5005,2,unit=1)
    Vdc=dec_to_float32(response.registers[0], response.registers[1])
    temp['F_Vdc'] = Vdc
   
    #Measure Iac_Ext
    response = client.read_input_registers(5021,2,unit=1)
    Iac_Ext=dec_to_float32(response.registers[0], response.registers[1])
    temp['G_Iac_Ext'] = Iac_Ext
    
    #Measure Vac_Out
    response = client.read_input_registers(5013,2,unit=1)
    Vac_Out=dec_to_float32(response.registers[0], response.registers[1])
    temp['H_Vac_Out'] = Vac_Out
    
    #Measure Choke Backplate
    #daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))
    #time.sleep(0.5)
    #temp['I_Choke_Backplate_Temp'] = float(daq.read())
    
    #Measure Choke Core
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@101'))
    time.sleep(0.5)
    temp['J_Choke_Core_Temp'] = float(daq.read())
    
    #Measure Choke Winding Bot
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@102'))
    time.sleep(0.5)
    temp['K_Choke_Winding_Bot_Temp'] = float(daq.read())
    
    #Measure Choke Top
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@103'))
    time.sleep(0.5)
    temp['L_Choke_Top_Temp'] = float(daq.read())
    
    #Measure T ambient
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@104'))
    time.sleep(0.5)
    temp['N_T_Amb'] = float(daq.read()) 
    
    #Measure Internal Temp
    response = client.read_input_registers(5093,2,unit=1)
    Int_Temp=dec_to_float32(response.registers[0], response.registers[1])
    temp['O_Int_Temp'] = Int_Temp
    
    #Measure Choke Winding Pad
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@105'))
    time.sleep(0.5)
    temp['P_Choke_Pad_Temp'] = float(daq.read())

    #Measure Int Ambient
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@106'))
    time.sleep(0.5)
    temp['Q_Int_Ambient_TC'] = float(daq.read())    


    
results = pd.DataFrame()
ref_time=time.time()
temp = {}
temp['C_PD']=0
while temp['C_PD'] !=1:
    
    #measure()
    try:
        measure()       
    except:
        try:
            print('measure error1')
            time.sleep(1)
            measure()
        except:
            try:
                print('measure error2')
                time.sleep(1)
                measure()
            except:
                print('measure error3')
                time.sleep(1)
                measure()
    
    results = results.append(temp, ignore_index=True)    # 17
    #print temp['A_Time'],' ',temp['E_Pac_Grid'],'Watts',' ',temp['C_PD'],' ',temp['D_SOC'],'%',' ',temp['I_Choke_Backplate_Temp'],'C',' ',temp['J_Choke_Core_Temp'],'C',' ',temp['K_Choke_Top_Temp'],'C',' ',temp['L_Trf_Pri_Temp'],'C',' ',temp['M_Trf_Sec_Temp'],'C'
    print temp['A_Time'],' ',temp['E_Pac_Grid'],'Watts',' ',temp['C_PD'],' ',temp['D_SOC'],'%',' ',temp['J_Choke_Core_Temp'],'C',' ',temp['K_Choke_Winding_Bot_Temp'],'C',' ',temp['L_Choke_Top_Temp'],'C',' ',temp['N_T_Amb'],'C',temp['O_Int_Temp'],'C',temp['P_Choke_Pad_Temp'],'C',' ',temp['Q_Int_Ambient_TC'],'C'
    results.to_csv('Unit2 with Option A shortened backplate Charge Discharge Additional Data.csv')
    time.sleep(60)   # Delay in seconds before capturing results               
print('finished')
