import os
import sys
import csv
import pandas as pd

inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/Data/PROSTATE 3-25-16 EE_FFPE#1 T-E&ARV7_GAPDH.csv'
outputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/Data/TEST_MOD.csv'

GUI_input = 'duplex'

def main(inputfile,GUI_input,outputfile):
# main function accepts filename, and GUI input. Options: 'duplex' or 'singleplex'

    # load as a dataframe
    df = pd.read_csv(inputfile, index_col=False)
    df['Target'].fillna('Blank', inplace=True) # replace NANs with 'Blank'

    # parse fullfilepath
    path, filename = os.path.split(inputfile)
    root, ext = os.path.splitext(filename)

    # fullfilepath for outputfile
    # create output filename with same root and path as input file, adding the suffix _MOD
    outputfile = path + '/' + root + '_MOD.csv'
    print('Output file = ' + outputfile)

    # ----- Error Checking #1 -----
    # (1) check to see if columns of interest exist
    if GUI_input == 'singleplex':
        # fieldnames to keep (singleplex samples)
        fnames_keep = ['Well', 'Sample', 'Target', 'CopiesPer20uLWell']
        for fname in fnames_keep:
            if fname not in df.columns:
                statusOut = ' Missing data columns! '
                statusColor = 'red'
                #return statusOut, statusColor
                print('Missing data columns!')
                sys.exit(1)

    elif GUI_input == 'duplex':
        # fieldnames to keep (duplex samples)
        fnames_keep = ['Well', 'Sample', 'TargetType', 'Target', 'CopiesPer20uLWell']
        for fname in fnames_keep:
            if fname not in df.columns:
                statusOut = ' Missing data columns!'
                statusColor = 'red'
                #return statusOut, statusColor
                print('Missing data columns!')
                sys.exit(1)
    print 'Input data is good'

    # (2) find duplicates in data
    dupl = df.duplicated(['Sample', 'TargetType', 'Target']) # output: bool

    dupl_df = df[dupl].sort_values('Sample') #data frame of duplicates in alphabetical order by sample
    dupl_indx = dupl_df.index.tolist()


    # rename duplicates
    if len(dupl_df) >= 1:
        #statusOut = ' Multiple duplicates found in data! '
        #statusColor = 'red'
        #return statusOut, statusColor
        print 'Duplicates found in data!'

        # loop through unique duplicated sample names
        count = 2 # initialize counter
        for i in range(len(dupl_df)):
            sampleName = df.loc[dupl_indx[i], 'Sample']


            if i != 0:
                #if sample name is same as previous, rename by appending _count
                if dupl_df.loc[dupl_indx[i],'Sample'] == dupl_df.loc[dupl_indx[i-1],'Sample']:
                    df.loc[dupl_indx[i], 'Sample'] = sampleName + '_' + str(count)
                    print('Renaming duplicate sample(s)to: ' + sampleName + '_' + str(count))
                    count = count + 1

                else:
                    count = 2
                    df.loc[dupl_indx[i], 'Sample'] = sampleName + '_' + str(count)
                    print('Renaming duplicate sample(s)to: ' + sampleName + '_' + str(count))
                    count = count + 1
            else: #for first element in sorted list (i = 0)
                df.loc[dupl_indx[i], 'Sample'] = sampleName + '_' + str(count)
                print('Renaming duplicate sample(s)to: ' + sampleName + '_' + str(count))
                count = count + 1

        df.to_csv(outputfile, columns=fnames_keep, index=False)

        #statusOut = 'Renaming duplicate sample(s) to:  ' + df.loc[dupl_indx,'Sample'].tolist()[0]
        #statusColor = 'red'
        #return statusOut, statusColor
    else:
        print 'No duplicates found'
        df.to_csv(outputfile, columns=fnames_keep, index=False)

        #sys.exit(1)

     # ----- End Error Checking -----

    # ------------------

    def addPivotTableToCSV(fullfilepath, GUI_input):

        df = pd.read_csv(fullfilepath) # load as a dataframe

        if GUI_input == 'singleplex':

            # pivot table
            pv_table = df.pivot_table(index='Sample', columns='Target', values='CopiesPer20uLWell')

            # merge original csv with new pivot table
            # first need to reset index of pv_table...
            pv_table = pv_table.reset_index()

            merged_data = pd.concat([df, pv_table], axis=1, join_axes=[df.index])
            merged_data.to_csv(fullfilepath, index=False)

        elif GUI_input == 'duplex':

            # ----- pivot tables -----
            # find indexes of Channel 1 data and Channel 2 data
            ch1_indx = df[df['TargetType'] == 'Ch1Unknown'].index.tolist()
            ch2_indx = df[df['TargetType'] == 'Ch2Unknown'].index.tolist()

            # OR...create multi-index
            #dfx = df.set_index(['TargetType','Sample])

            # create table 1 (ch1)
            pv_table1 = df.ix[ch1_indx].pivot(index='Sample', columns='Target', values='CopiesPer20uLWell')
            pv_table1 = pv_table1.reset_index() # reset index to numeric (0,1,2,3,...)

            # create table 2 (ch2)
            pv_table2 = df.ix[ch2_indx].pivot(index='Sample', columns='Target', values='CopiesPer20uLWell')
            pv_table2 = pv_table2.reset_index()  # reset index to numeric (0,1,2,3,...)

            # Row concatenate tables
            # first renumber pv_table2 index...
            x = len(pv_table1) + 2 # add extra rows to separate the two tables
            pv_table2.index = range(x, len(pv_table2)+x)

            # get column headings for table 2
            pv_table2_header = pv_table2.columns.tolist()

            # rename Sample column to Sample_Ch2
            pv_table2_header[0] = 'Sample_Ch2'
            pv_table2.ix[x - 1, :] = pv_table2_header

            # concatenate Ch1 and Ch2 tables
            pv_table = pd.concat([pv_table1, pv_table2], axis=0).sort_index()

            pv_table.rename(columns={'Sample': 'Sample_Ch1'}, inplace=True)  # rename Sample column to Ch1
            #pv_table.to_csv('/Users/lindanieman/Documents/WORK/MGH CC/Droplets/Data/TEST.csv', index=True)

            # for "duplex" data that is not paired (i.e. ch1 and ch2 have different targets and/or samples)
            if sum(pv_table2.columns.isin(pv_table1.columns)) != len(pv_table2_header):
                # concatenate column header for all
                # get column headings for table 1
                pv_table1.rename(columns={'Sample': 'Sample_Ch1'}, inplace=True)  # rename Sample column to Ch1
                header = df.columns.tolist() + pv_table1.columns.tolist() + pv_table2_header[1:]
            else:
                header = df.columns.tolist() + pv_table.columns.tolist()



            # merge original csv with new pivot table
            merged_data = pd.concat([df, pv_table], axis=1, join_axes=[df.index])
            merged_data = merged_data.ix[:,header] #re-order columns
            merged_data.to_csv(fullfilepath, index=False)


    if outputfile == None:
        foo = None
        return 0  # this is needed to communicate the completion status of this process to the outside world
        # 0, process not complete, file not chosen...

    else:
        #writeShortCSV(outputfile, fnames_keep)
        #print 'test'
        addPivotTableToCSV(outputfile, GUI_input)
        #statusOut = ' Done!  Output file: ' + root + '_MOD.csv'
        #statusColor = 'darkgreen'
        #return statusOut, statusColor
        # means the process is complete, the external GUI is able to report "Done" status writing in green color


if __name__ == "__main__":
    main(inputfile,GUI_input,outputfile)











