import pandas as pd

#filename='64V_DC_Input.csv'
filename='Eficiency_Test_Reference_Duncan_Discharge'

sample_data=pd.read_csv(filename+'.csv')
data = pd.DataFrame()

#max_col = sample_data.shape[0]
max_col = sample_data.shape[0]-1
#print max_col

cntr=0

while cntr<max_col:
    if (sample_data.Watts_AC.iloc[cntr]-sample_data.Watts_AC.iloc[cntr+1])<300:
        #print (sample_data.Watts_AC.iloc[cntr+1]-sample_data.Watts_AC.iloc[cntr])
        cntr=cntr+1
        #print ('run')
        #print cntr
    else:
        print cntr
        print sample_data.Watts_AC.iloc[cntr]
        print (sample_data.Watts_AC.iloc[cntr]-sample_data.Watts_AC.iloc[cntr+1])
        cntr=cntr+1
        temp=sample_data[["Taken","Vrms","Arms","Watts_AC","PF","Freq","Athd","Watts_DC","Vdc","Adc"]].iloc[(cntr-11):(cntr-1)]
        data=data.append(temp, ignore_index=True)

data.to_csv(filename+'_Processed'+'.csv')
print ('done')