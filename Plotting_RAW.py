import os
import pandas as pd
import matplotlib.pyplot as plt
plt.ioff() # turn off intereactive mode so will only display figures if explicitly called
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/MelRawDropletData_20160615.csv'
outputdir = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/MelData/PlotOutput/2016-06-15/Patient_withFAT1/'


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

    ### removed first element:  'FAT1-1'
    markers = pd.DataFrame(['FAT1','GRP143', 'IL13RA2', 'MAGEA2', 'MAGEC2', 'PMEL', 'SFRP1', 'TFAP2C', 'TNC', 'CSPG4', 'FAT2', 'GAGE1', 'MAGEA1', 'MAGEA4', 'MAGEA6', 'MLANA', 'PRAME', 'SOX10', 'TYRP1']);
    markersTotals = pd.DataFrame(['TotalTranscriptsPerWellPerMlBlood', 'LineageSpecific', 'CarcinoEmbryonicAntigen', 'SignalTransduction']);
    markers.rename(columns={0: 'Marker'}, inplace=True) # rename column
    markersTotals.rename(columns={0: 'MarkersTotals'}, inplace=True) # rename column


    # loop through each unique patient and plot time series
    #patients = ['PEM01']
    for p in patients:
        print 'patient= ' + p
        #p = 'PEM01'
        pData = df.loc[df.Patient_ID == p]

        #with PdfPages(outputdir + p + '_Log2.pdf') as pdf: # LOG2
        with PdfPages(outputdir + p + '_RAW.pdf') as pdf:  # RAW

            fig = plt.figure(figsize=(12,8))
            plt.suptitle(p + '\n Copies/mL vs. Time (weeks)', fontsize=14, fontweight='bold') #Log2(Copies/mL + 1)

            # -------------------------------------------------
            # plot each marker separately as a function of time
            for m in xrange(0,len(markers)): #(start,stop,step)

                if len(markers) <= 20:

                    plt.subplot(5,4,m+1)
                    x=pData.TimeFromInitialBloodDraw_weeks
                    y=pData[markers.ix[m][0]] # RAW
                    #y = np.log2(pData[markers.ix[m][0]] +1) # LOG2
                    plt.plot(x, y, '-ro', markersize=10)

                    #plt.ylabel('log2(' + markers.ix[m][0] + ') \n (copies / mL)', fontsize = 8) # LOG2
                    plt.ylabel(markers.ix[m][0] + ' Copies / mL', fontsize=8) # RAW
                    plt.ylim(ymin=0)

                    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.4)
                    ax = plt.gca()
                    ax.tick_params(axis='y', labelsize=6)
                    ax.tick_params(axis='x', labelsize=8)

                    #ax.ticklabel_format(axis='y', style='sci', scilimits=(-2,2), useOffset=True)

                else:
                    print 'Number of markers is greater than 20! \Modify for loop code'

            pdf.savefig()
            plt.close()
            #plt.show()

            # ---------------------------------------------------------------------
            # plot totals, lineaage specific, carcinoembryonic, signaltransduction
            fig = plt.figure()
            plt.suptitle(p + '\n Copies/mL vs. Time (weeks)', fontsize=14, fontweight='bold') # RAW
            for n in xrange(0,len(markersTotals)):

                plt.subplot(2,2,n+1)
                x = pData.TimeFromInitialBloodDraw_weeks
                y = pData[markersTotals.ix[n][0]] # RAW
                #y = np.log2(pData[markersTotals.ix[n][0]] +1) # LOG2
                plt.plot(x, y, '-ro')
                plt.ylim(ymin=0)
                plt.title(markersTotals.ix[n][0], fontsize=12)
                #plt.ylabel('log2(x+1)' + '\n (copies / mL)', fontsize=12) # LOG2
                plt.ylabel('Copies / mL', fontsize=12)  # 'RAW'

                plt.subplots_adjust(left=0.15, bottom=None, right=0.95, top=0.85, wspace=0.5, hspace=0.4)
                ax = plt.gca()
                ax.tick_params(axis='y', labelsize=8)
                ax.tick_params(axis='x', labelsize=8)

                ## add ClinicalClassification annotation
                ccLabels = pData.ClinicalClassification.reset_index().ix[:,1].tolist() #label list for given patient

                # for label, X, Y in zip(ccLabels, x, y):
                #     plt.annotate(label, xy=(X,Y), xytext=(-20,20), textcoords='offset points',
                #                  ha='left', va='bottom', bbox = dict(boxstyle = 'round,pad=0.25', fc = 'yellow', alpha = 0.50),
                #                  arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'),fontsize=8)

            #plt.show()
            pdf.savefig()
            plt.close()

        #p = 'PEM-15'
        #pData = df.loc[df.Patient_ID == p]

            def stackedBarPlots(pData, markers):
                # this function plots a stacked bar graph

                markers.sort_values('Marker', axis=0, inplace=True)  # sort markers names alphabetically
                markers.reset_index(drop=True, inplace=True)

                fig_bar = plt.figure(figsize=(10, 8))
                plt.subplot(211)

                bar_x = np.arange(len(pData.TimeFromInitialBloodDraw_weeks)) + 0.2
                barWidth = 0.75
                y_offset = np.array([0.0] * len(bar_x))

                # Get colors for bars
                colors = plt.cm.Set1(np.linspace(0, 0.75, len(markers)))

                #cell_text2 = []
                for m in xrange(0, len(markers)):  # (start,stop,step)
                    #print('marker = ' + marker.ix[m])

                    if len(markers) <= 20:
                        y = pData[markers.ix[m][0]]
                        #y = np.log2(pData[markers.ix[m][0]] + 1)  # take log2(x+1)
                        plt.bar(bar_x, y, barWidth, bottom=y_offset, color=colors[m], label=markers.ix[m, 'Marker'])
                        y_offset = y_offset + y

                    else:
                        print 'Number of markers is greater than 20! \Modify for loop code'

                plt.ylabel('log2(x+1)' + '\n (copies / mL)', fontsize=16)
                #plt.ylabel('Copies / mL', fontsize=16)
                plt.xlabel('Time (weeks)', fontsize=16)
                plt.title(p, fontsize=18)
                plt.xticks(pd.Series(bar_x) + barWidth / 2, pData.TimeFromInitialBloodDraw_weeks)
                plt.subplots_adjust(left=0.15, bottom=None, right=0.82, top=None, wspace=None, hspace=None)
                plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0,
                           fontsize=10)  # colors,markersSorted['Marker'])
                ax1 = plt.gca()
                ax1.set_yscale('log',nonposy='clip')
                plt.ylim(ymin=0.1)


                plt.subplot(212)
                ax = plt.gca()
                ax.axis('off')
                cellTEXT = [[txt] for txt in pData.ClinicalAnnotations]
                rowLABELS = [(str(rtxt) + ' weeks') for rtxt in pData.TimeFromInitialBloodDraw_weeks.tolist()]
                colLABELS = ['Clinical Annotation']
                the_table = plt.table(cellText=cellTEXT, colLabels=colLABELS, rowLabels=rowLABELS, loc='center',
                                      cellLoc='center')
                # or the_table = ax.table(...)
                the_table.set_fontsize(12)
                the_table.scale(1, 2)
                table_props = the_table.properties()
                table_cells = table_props['child_artists']


            stackedBarPlots(pData,markers)

            #plt.show()
            pdf.savefig()
            plt.close()

    if outputdir == None:
        foo = None
        return 0  # this is needed to communicate the completion status of this process to the outside world
        # 0, process not complete, file not chosen...

    else:
        print 'test'
        stackedBarPlots(pData, markers)
        #     statusDoneOut = ' Done!  >>> Output file: ' + root + '_MOD.csv'
        #     statusDoneColor = 'darkgreen'
        #
        #     return statusOut, statusColor, statusDoneOut, statusDoneColor


    #plt.close('all')

#
if __name__ == "__main__":
    main(inputfile, outputdir)
