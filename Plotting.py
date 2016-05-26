import os
#import sys
#import csv
import pandas as pd
import matplotlib.pyplot as plt

inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/MelRawDropletData_20160526.csv'
outputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/MelRawDropletData_20160526_mod.csv'

# load as a dataframe
df = pd.read_csv(inputfile, index_col=False)
df.dropna(how='all', inplace=True) # remove blank rows
#df['Target'].fillna('Blank', inplace=True) # replace column NANs with 'Blank'
colNames = df.columns.tolist()
patients = df.Patient_ID.unique()
df['DrawDate'] = pd.to_datetime(df['DrawDate'],infer_datetime_format=True) #change datetime to python friendly format


# parse fullfilepath
path, filename = os.path.split(inputfile)
root, ext = os.path.splitext(filename)

markers = pd.DataFrame(['FAT1-1', 'GRP143', 'IL13RA2', 'MAGEA2', 'MAGEC2', 'PMEL', 'SFRP1', 'TFAP2C', 'TNC', 'CSPG4', 'FAT2', 'GAGE1',\
           'MAGEA1', 'MAGEA4', 'MAGEA6', 'MLANA', 'PRAME', 'SOX10', 'TYRP1', 'TotalDropletsPerMLblood', 'LineageSpecific',\
           'CarcinomebryonicAntigen', 'SignalTransduction']);
markers.rename(columns={0: 'Marker'}, inplace=True) # rename column



# loop through each unique patient and plot time series
 for p in patients:

     p = 'PEM-15'
     for m in range(len(markers)):

         #m=3
         plt.figure(m)
         pData = df.loc[df.Patient_ID == p]
         plt.plot(pData.TimeFromInitialBloodDraw_weeks, pData[markers[m]], '-ro', markersize=12)
         plt.ylabel(markers[m] + ' (copies / mL)')
         plt.xlabel('Time from initial blood draw (weeks)')
         plt.title(p)


 plt.close('all')

     # get date




#
# if __name__ == "__main__":
#     main(inputfile, GUI_input)











