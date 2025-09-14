import os
import pickle
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


localData = '/scratch/tolugboj_lab/Prj5_HarnomicRFTraces/AkiEstimate/tutorial/Results/ResultOf03_03/'

# Run through all station pairs in the list
df = pd.read_csv('Genconn.csv')

pred_RPVs = np.zeros((len(df), 2880))
pred_LPVs = np.zeros((len(df), 2880))

AkiEstexist = np.zeros(len(df))

for index, row in df.iterrows():
    
    stapair = row['net1']+'-'+row['sta1']+'_'+row['net2']+'-'+row['sta2']

    file_path = localData + 'Final_' + stapair + '/opt.pred-love'
    if os.path.exists(file_path):
    
        # read in AkiEstimate Results
        pred_f = []
        pred_LPV = []
        # pred_LJ0 = []
        with open(file_path, 'r') as f:
            for line in f:
                # Split on whitespace
                tokens = line.split()
                
                # Convert each token to float
                floats = [float(tok) for tok in tokens]
                pred_f.append(floats[0])
                pred_LPV.append(floats[2]/1000)
                # pred_LJ0.append(floats[5])
        
        pred_LPVs[index, :] = pred_LPV[0:2880]
        
        pred_RPV = []
        # pred_RJ0 = []
        with open(localData + 'Final_' + stapair + '/opt.pred-rayleigh', 'r') as f:
            for line in f:
                # Split on whitespace
                tokens = line.split()
                
                # Convert each token to float
                floats = [float(tok) for tok in tokens]
                pred_RPV.append(floats[2]/1000)
                # pred_RJ0.append(floats[5])
    
        pred_RPVs[index, :] = pred_RPV[:2880]

        AkiEstexist[index] = 1

with open('./GenTestAkiNet.pkl', 'rb') as file:
    AkiNet = pickle.load(file)

AkiNetR = AkiNet[0][AkiEstexist.astype(bool), :]
AkiNetL = AkiNet[1][AkiEstexist.astype(bool), :]

# read in the Love PV for the AK135 model
file_path = './SDISPL.ASC' 
df = pd.read_csv(file_path, sep='\s+')
PREM_Lf = np.array(df['FREQUENCY(Hz)'][df['LMODE'] == 0])
PREM_LPV = np.array(df['C(KM/S)'][df['LMODE'] == 0])

# read in the Rayleigh PV for the AK135 model
file_path = './SDISPR.ASC'  
df = pd.read_csv(file_path, sep='\s+')
PREM_Rf = np.array(df['FREQUENCY(Hz)'][df['RMODE'] == 0])
PREM_RPV = np.array(df['C(KM/S)'][df['RMODE'] == 0])

matplotlib.rcParams.update({'font.size': 9})
fig, axes = plt.subplots(1,2, figsize=(7.5, 3), dpi=80, sharey=True,
                        gridspec_kw = dict( left = 0.08, right = 0.96, bottom = 0.15, top = 0.95, wspace = 0.15))

###### plot the Rayleigh distribution ######
# Put into a DataFrame
data1 = AkiNetR[:, 360]
data2 = pred_RPVs[:, 719]
data3 = AkiNetR[:, 1080]
data4 = pred_RPVs[:, 1439]
data5 = AkiNetR[:, 1800]
data6 = pred_RPVs[:, 2159]
data7 = AkiNetR[:, 2520]
data8 = pred_RPVs[:, 2879]

RayPVs = pd.DataFrame({
    "c(f) [km/s]": np.concatenate([data1, data2, data3, data4, data5, data6, data7, data8]),
    "Method": ["AkiNet"]*len(data1) + ["AkiEstimate"]*len(data2) + ["AkiNet"]*len(data3) + ["AkiEstimate"]*len(data4) 
    + ["AkiNet"]*len(data5) + ["AkiEstimate"]*len(data6) + ["AkiNet"]*len(data7) + ["AkiEstimate"]*len(data8),
    "Frequency [Hz]": ["0.05"]*(len(data1)+len(data2)) + ["0.1"]*(len(data3)+len(data4)) + ["0.15"]*(len(data5)+len(data6)) + ["0.2"]*(len(data7)+len(data8))
})

# Plot split violin
vio1 = sns.violinplot(x="Frequency [Hz]", y="c(f) [km/s]", hue="Method", data=RayPVs, 
    split=True,   # <-- split halves!
    common_norm=True,      # same max width per violin
    inner="quartile", # show median & quartiles
    palette={"AkiNet":"lightcoral", "AkiEstimate":"skyblue"}, ax=axes[0], linewidth=0.7)
vio1.legend_.set_title(None)

# interpolate the AK135 frequency to the sns violin plot
axes[0].plot((PREM_Rf[:-25]-0.05)*10*2, PREM_RPV[:-25], 'k:')
axes[0].set_xlim([-0.5, 3.5])
axes[0].text(-0.4, 6.7, '(a)', fontsize=11, color='k')

###### plot the Love distribution ######
# Put into a DataFrame
data1 = AkiNetL[:, 360]
data2 = pred_LPVs[:, 719]
data3 = AkiNetL[:, 1080]
data4 = pred_LPVs[:, 1439]
data5 = AkiNetL[:, 1800]
data6 = pred_LPVs[:, 2159]
data7 = AkiNetL[:, 2520]
data8 = pred_LPVs[:, 2879]

LovePVs = pd.DataFrame({
    "c(f) [km/s]": np.concatenate([data1, data2, data3, data4, data5, data6, data7, data8]),
    "Method": ["AkiNet"]*len(data1) + ["AkiEstimate"]*len(data2) + ["AkiNet"]*len(data3) + ["AkiEstimate"]*len(data4) 
    + ["AkiNet"]*len(data5) + ["AkiEstimate"]*len(data6) + ["AkiNet"]*len(data7) + ["AkiEstimate"]*len(data8),
    "Frequency [Hz]": ["0.05"]*(len(data1)+len(data2)) + ["0.1"]*(len(data3)+len(data4)) + ["0.15"]*(len(data5)+len(data6)) + ["0.2"]*(len(data7)+len(data8))
})

# Plot split violin
vio2 = sns.violinplot(x="Frequency [Hz]", y="c(f) [km/s]", hue="Method", data=LovePVs, 
    split=True,   # <-- split halves!
    common_norm=True,      # same max width per violin
    inner="quartile", # show median & quartiles
    palette={"AkiNet":"lightcoral", "AkiEstimate":"skyblue"}, ax=axes[1], legend=False, linewidth=0.7)

# interpolate the AK135 frequency to the sns violin plot
axes[1].plot((PREM_Lf[:-25]-0.05)*10*2, PREM_LPV[:-25], 'k:')
axes[1].set_xlim([-0.5, 3.5])
axes[1].text(-0.4, 6.7, '(b)', fontsize=11, color='k')

plt.savefig( './Fig6_GenTest.pdf', dpi = 400, facecolor = 'w' )

 
