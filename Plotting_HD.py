import os
import pandas as pd
import matplotlib.pyplot as plt
plt.ioff() # turn off intereactive mode so will only display figures if explicitly called
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/MelRawDropletData_20160607_HD.csv'
outputdir = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/PlotOutput/2016-06-07/HD/'


def main(inputfile,outputdir):

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

    # removed:  'FAT1-1',
    markers = pd.DataFrame(['GRP143', 'IL13RA2', 'MAGEA2', 'MAGEC2', 'PMEL', 'SFRP1', 'TFAP2C', 'TNC', 'CSPG4', 'FAT2', 'GAGE1', 'MAGEA1', 'MAGEA4', 'MAGEA6', 'MLANA', 'PRAME', 'SOX10', 'TYRP1']);

    markersTotals = pd.DataFrame(['TotalTranscriptsPerWellPerMlBlood', 'LineageSpecific', 'CarcinoEmbryonicAntigen', 'SignalTransduction']);
    markers.rename(columns={0: 'Marker'}, inplace=True) # rename column
    markersTotals.rename(columns={0: 'MarkersTotals'}, inplace=True) # rename column
    markers.sort_values('Marker', axis=0, inplace=True)  # sort markers names alphabetically
    markers.reset_index(drop=True, inplace=True)

    #pData = df.loc[df.Patient_ID == p]

    #with PdfPages(outputdir + p + '_Log2.pdf') as pdf: # LOG2
    with PdfPages(outputdir + 'HealthyDonors' + '_log2_NoFAT1.pdf') as pdf:  # RAW

        fig1 = plt.figure(figsize=(12,8))
        plt.suptitle('Healthy Donors, copies/mL', fontsize=14, fontweight='bold')

        # -------------------------------------------------
        # plot each marker separately
        for m in xrange(0,len(markers)): #(start,stop,step)

            if len(markers) <= 20:

                plt.subplot(5,4,m+1)
                bar_x = np.arange(len(df.Patient_ID)) + 0.2
                #y=df.ix[:,markers.ix[m][0]] # RAW
                y = np.log2(df.ix[:,markers.ix[m][0]] +1) # LOG2
                plt.bar(bar_x, y)

                plt.ylabel('log2(' + markers.ix[m][0] + ') \n (copies / mL)', fontsize = 8) # LOG2
                #plt.ylabel(markers.ix[m][0], fontsize=10) # RAW
                plt.ylim(ymin=0)

                plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.4)
                ax = plt.gca()
                #ax.set_xticklabels(df.Patient_ID.tolist())
                ax.tick_params(axis='y', labelsize=6)
                ax.tick_params(axis='x', labelsize=8)

            else:
                print 'Number of markers is greater than 20! \Modify for loop code'

        pdf.savefig()
        plt.close()
        #plt.show()

        # ---------------------------------------------------------------------
        # plot totals, lineaage specific, carcinoembryonic, signaltransduction
        fig2 = plt.figure()
        plt.suptitle('Healthy Donors', fontsize=14, fontweight='bold') # RAW
        #plt.suptitle(p + '\n Copies/mL vs. Time (weeks)', fontsize=14, fontweight='bold')  # LOG2
        for n in xrange(0,len(markersTotals)):

            plt.subplot(2,2,n+1)
            #y = df.ix[:, markersTotals.ix[n][0]]  # RAW
            y = np.log2(df[markersTotals.ix[n][0]] +1) # LOG2
            plt.bar(bar_x, y)
            plt.ylim(ymin=0)
            plt.title(markersTotals.ix[n][0], fontsize=12)
            plt.ylabel('log2(x+1)' + '\n (copies / mL)', fontsize=12) # LOG2
            #plt.ylabel('Copies / mL', fontsize=12)  # 'RAW'

            plt.subplots_adjust(left=0.15, bottom=None, right=0.95, top=0.85, wspace=0.5, hspace=0.4)
            ax = plt.gca()
            ax.tick_params(axis='y', labelsize=8)
            ax.tick_params(axis='x', labelsize=8)

        #plt.show()
        pdf.savefig()
        plt.close()

        def stackedBarPlots(pData, markers):
            # this function plots a stacked bar graph

            fig_bar = plt.figure(figsize=(12, 8))
            plt.title('Healthy Donors', fontsize=18)
            plt.ylabel('Copies / mL', fontsize=16)


            # Get colors for bars
            colors = plt.cm.Set1(np.linspace(0, 0.75, len(markers)))

            # define x axis
            bar_x = np.arange(len(patients)) + 0.2
            barWidth = 0.75

            #for p in xrange(0,len(patients)): # (start,stop,step)
             #   pData = df.loc[df.Patient_ID == p]

            y_offset = np.array([0.0] * len(patients))

            if len(markers) <= 20:

                for m in xrange(0, len(markers)):  # (start,stop,step)
                    #print('marker = ' + marker.ix[m])

                        #y = df[markers.ix[m][0]]  # RAW
                        y = np.log2(df[markers.ix[m][0]] + 1)  # take log2(x+1)
                        plt.bar(bar_x, y, barWidth, bottom=y_offset, color=colors[m], label=markers.ix[m, 'Marker'])
                        y_offset = y_offset + y
            else:
                print 'Number of markers is greater than 20! \Modify for loop code'

            plt.subplots_adjust(left=0.15, bottom=None, right=0.82, top=None, wspace=None, hspace=None)
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, fontsize=10)  # colors,markersSorted['Marker'])
            ax1 = plt.gca()
            #ax1.set_yscale('log',nonposy='clip')
            plt.xticks(bar_x+barWidth/2,np.arange(0,len(patients))+1)
            #ax1.set_ylim(ymin=0.1)
            #plt.ylim(ymin=0.1) # RAW
            plt.ylim(ymin=0)
        stackedBarPlots(df,markers)

        #plt.show()
        pdf.savefig()
        plt.close()

    if outputdir == None:
        foo = None
        return 0  # this is needed to communicate the completion status of this process to the outside world
        # 0, process not complete, file not chosen...

    else:
        print 'test'
        stackedBarPlots(df, markers)
        #     statusDoneOut = ' Done!  >>> Output file: ' + root + '_MOD.csv'
        #     statusDoneColor = 'darkgreen'
        #
        #     return statusOut, statusColor, statusDoneOut, statusDoneColor


        #plt.close('all')

#
if __name__ == "__main__":
    main(inputfile, outputdir)