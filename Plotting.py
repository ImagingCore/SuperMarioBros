import os
#import sys
#import csv
import pandas as pd
import matplotlib.pyplot as plt
plt.ioff() # turn off intereactive mode so will only display figures if explicitly called
from matplotlib.backends.backend_pdf import PdfPages


inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/MelRawDropletData_20160526.csv'
outputdir = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/PlotOutput/'

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

markers = pd.DataFrame(['FAT1-1', 'GRP143', 'IL13RA2', 'MAGEA2', 'MAGEC2', 'PMEL', 'SFRP1', 'TFAP2C', 'TNC', 'CSPG4', 'FAT2', 'GAGE1', \
                        'MAGEA1', 'MAGEA4', 'MAGEA6', 'MLANA', 'PRAME', 'SOX10', 'TYRP1']);
markersTotals = pd.DataFrame([ 'TotalDropletsPerMLblood', 'LineageSpecific', 'CarcinomebryonicAntigen', 'SignalTransduction']);
markers.rename(columns={0: 'Marker'}, inplace=True) # rename column
markersTotals.rename(columns={0: 'MarkersTotals'}, inplace=True) # rename column

# loop through each unique patient and plot time series
for p in patients:

    p = 'PEM-15'
    # pp = PdfPages('/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/PlotOutput/' + p + '_plots.pdf')

    with PdfPages(outputdir + p + '_plots.pdf') as pdf:

        fig = plt.figure(figsize=(12,8))
        plt.suptitle(p + '\n Copies/mL vs. Time (weeks)', fontsize=14, fontweight='bold')

        for m in xrange(0,len(markers)): #(start,stop,step)

            if len(markers) <= 20:
                pData = df.loc[df.Patient_ID == p]

                plt.subplot(5,4,m+1)
                plt.plot(pData.TimeFromInitialBloodDraw_weeks, pData[markers.ix[m][0]], '-ro', markersize=10)

                plt.ylabel(markers.ix[m][0] + '\n (copies / mL)', fontsize = 8)
                #plt.xlabel('Time (weeks)', fontsize=8)

                plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.4)
                ax = plt.gca()
                ax.tick_params(axis='y', labelsize=6)
                #ax.ticklabel_format(axis='y', style='sci', scilimits=(-2,2), useOffset=True)

            else:
                print 'Number of markers is greater than 20! \Modify for loop code'

        pdf.savefig()
        plt.close()
        # plt.show()

        fig = plt.figure()
        plt.suptitle(p + '\n Copies/mL vs. Time (weeks)', fontsize=14, fontweight='bold')
        for n in xrange(0,len(markersTotals)):

            plt.subplot(2,2,n+1)
            plt.plot(pData.TimeFromInitialBloodDraw_weeks, pData[markersTotals.ix[n][0]], '-ro')
            plt.title(markersTotals.ix[n][0], fontsize=12)
            #plt.ylabel(markersTotals.ix[n][0] + '\n (copies / mL)', fontsize=12)

            plt.subplots_adjust(left=0.15, bottom=None, right=0.95, top=0.85, wspace=0.5, hspace=0.4)
            ax = plt.gca()
            ax.tick_params(axis='y', labelsize=8)

        #plt.show()
        pdf.savefig()
        plt.close()

# add marker different marker colors for TN, PD, RD, etc
# log2 normalization
# create stacked bar graphs
# add clinical annotations




#plt.close('all')






#
# if __name__ == "__main__":
#     main(inputfile, GUI_input)











