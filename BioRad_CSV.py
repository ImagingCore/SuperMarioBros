import os
import sys
import csv
import pandas as pd

inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/Data/Prostate_test_noBlanks-SingleMultipleDup.csv'
GUI_input = 'duplex'

def main(inputfile,GUI_input):
# main function accepts filename, and GUI input. Options: 'duplex' or 'singleplex'


    # load as a dataframe
    df = pd.read_csv(inputfile, index_col=False)

    # parse fullfilepath
    path, filename = os.path.split(inputfile)
    root, ext = os.path.splitext(filename)

    # fullfilepath for outputfile
    # create output filename with same root and path as input file, adding the suffix _MOD
    outputfile = path + '/' + root + '_MOD.csv'

    print outputfile

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

    #dupl_indx = dupl[(dupl == 1)].index.tolist() # record index of duplicates

    #dupl_samples = dupl_df['Sample'].unique().tolist().sort() # list of unique names of duplicated samples in alphabetical order
    #dupl_size = df.groupby(['Sample', 'TargetType', 'Target']).size()

    # rename duplicates
    if len(dupl_indx) >= 2:
        #statusOut = ' Multiple duplicates found in data! '
        #statusColor = 'red'
        #return statusOut, statusColor
        print 'Duplicates found in data!'

        #sampleName = df.loc[dupl_indx,'Sample']
        #dupl_df = df.loc[dupl_indx,'Sample'].to_frame()
        #dupl_df[dupl_df['Sample'] == 'H2O']

        # loop through unique (duplicated) sample names
        count = 2 # initialize counter
        for i in range(len(dupl_df)):
            sampleName = df.loc[dupl_indx[i], 'Sample']

            if i != 0:
                #if sample name is same as previous, append _count
                if dupl_df.loc[dupl_indx[i],'Sample'] == dupl_df.loc[dupl_indx[i-1],'Sample']:

                    df.loc[dupl_indx[i], 'Sample'] = sampleName + '_' + str(count)
                    print('Renaming duplicate sample(s)to: ' + sampleName + '_' + str(count))

                    count = count + 1

                else:
                    df.loc[dupl_indx[i], 'Sample'] = sampleName + '_' + str(count)
                    count = count + 1

            else:
                df.loc[dupl_indx[i], 'Sample'] = sampleName + '_' + str(count)

            #dupl_sample = dupl_size[dupl_size > 2].index.tolist() #find unique duplicated elements. index contains: sample, targettype, target
            #len(df[df['Sample'] == test[0][0]]) # [0][0] is the sample name of the first unique repeat

            # Loop through all repeats for a given sample name
            #for j in range(len(dupl_sample)):

                # rename all samples with same name
              #  df[df['Sample']==dupl_sample[i][j]]

        #sys.exit(1)
    #elif len(dupl_size[dupl_size == 2]):  #(len(dupl_indx) == 1):
     #   sampleName = df.loc[dupl_indx, 'Sample']
      #  df.loc[dupl_indx, 'Sample'] = sampleName + '_' + str(2)
        df.to_csv(outputfile, columns = fnames_keep)

        #print('Renaming duplicate sample(s) to: ' + df.loc[dupl_indx,'Sample'].tolist()[0])

        #statusOut = 'Renaming duplicate sample(s) to:  ' + df.loc[dupl_indx,'Sample'].tolist()[0]
        #statusColor = 'red'
        #return statusOut, statusColor
    else:
        print 'No duplicates found'
        df.to_csv(outputfile, colunns = fnames_keep)

    print 'duplicates check'
        #sys.exit(1)

     # ----- End Error Checking -----


# DON'T NEED THIS METHOD:
    def writeShortCSV(outputfile,fnames_keep):

        with open(outputfile, 'w') as csvoutfile: # open output file
            writer = csv.DictWriter(csvoutfile,fieldnames=fnames_keep,extrasaction='ignore')
            writer.writeheader()

            with open(inputfile, 'rU') as csvfile: # open input file
                reader = csv.DictReader(csvfile) # read csv file
                # creates dict of the form:  {key, value} = {Column_header, value}

                for row in reader:   # iterate over rows, each row is a dict
                    writer.writerow(row)

    # ------------------

    # ------------------
    def getUniqueValues(fullfilepath):

        with open(fullfilepath, 'rU') as csvfile: # open input file
            reader = csv.DictReader(csvfile) # read csv file
            # create dict of the form:  {key, value} = {Column_header, value}

            unique_targets = set() # only contains unique items
            unique_samples = set()

            for row in reader:   # iterate over rows, each row is a dict

                unique_targets.add(row['Target'])
                unique_samples.add(row['Sample'])

        return unique_samples, unique_targets
     # ---------------------

    #getUniqueValues(modifiedFile)


    # --------------------------


    def addPivotTableToCSV(fullfilepath, GUI_input):

        df = pd.read_csv(fullfilepath) # load as a dataframe


        if GUI_input == 'singleplex':
            # find duplicates in data
            # dupl = df.duplicated(['Sample','Target'])
            # dupl_indx = dupl[(dupl == 1)].index.tolist()
            #
            # # rename single duplicate, alert user if there is more than one duplicate
            # if len(dupl_indx) > 1:
            #     print 'Multiple duplicates found in data!'
            #     sys.exit(1)
            # elif (len(dupl_indx) == 1):
            #     sampleName = df.loc[dupl_indx,'Sample']
            #     df.loc[dupl_indx,'Sample'] = sampleName + '-' + str(2)
            #     print('Duplicate renamed to: ' + df.loc[dupl_indx,'Sample'])

            # pivot table
            pv_table = df.pivot_table(index='Sample', columns='Target', values='CopiesPer20uLWell')

            # merge original csv with new pivot table
            # first need to reset index of pv_table...
            pv_table = pv_table.reset_index()

            merged_data = pd.concat([df, pv_table], axis=1, join_axes=[df.index])
            merged_data.to_csv(fullfilepath)

        elif GUI_input == 'duplex':
            # find duplicates in data
            # dupl = df.duplicated(['Sample','TargetType','Target'])
            # dupl_indx = dupl[(dupl == 1)].index.tolist()
            #
            # # rename single duplicate, alert user if there is more than one duplicate
            # if len(dupl_indx) > 1:
            #     print 'Multiple duplicates found in data!'
            #     print dupl
            #     sys.exit(1)
            # elif (len(dupl_indx) == 1):
            #     sampleName = df.loc[dupl_indx, 'Sample']
            #     df.loc[dupl_indx, 'Sample'] = sampleName + '-' + str(2)
            #     print('Duplicate renamed to: ' + df.loc[dupl_indx, 'Sample'])


            # ----- pivot tables -----
            # find indexes of Channel 1 data and Channel 2 data
            ch1_indx = df[df['TargetType'] == 'Ch1Unknown'].index.tolist()
            ch2_indx = df[df['TargetType'] == 'Ch2Unknown'].index.tolist()

            # OR...create multi-index
            #dfx = df.set_index(['Sample','TargetType'])


            # create table 1 (ch1)
            pv_table1 = df.ix[ch1_indx].pivot(index='Sample', columns='Target', values='CopiesPer20uLWell')
            pv_table1 = pv_table1.reset_index() # reset index to numerical (0,1,2,3,...)

            # create table 2 (ch2)
            pv_table2 = df.ix[ch2_indx].pivot(index='Sample', columns='Target', values='CopiesPer20uLWell')
            pv_table2 = pv_table2.reset_index()  # reset index to numerical (0,1,2,3,...)

            # Row concatenate tables
            # first renumber pv_table2 index...
            x = len(pv_table1) + 2 # add extra rows to separate the two tables
            pv_table2.index = range(x, len(pv_table2)+x)

            # rename Sample column to Sample_Ch2
            header = pv_table1.columns.tolist()
            header[0] = 'Sample_Ch2'
            pv_table2.ix[x-1,:]=header

            #concatenate Ch1 and Ch2 tables
            pv_table = pd.concat([pv_table1, pv_table2], axis=0)
            pv_table.rename(columns={'Sample':'Sample_Ch1'}, inplace=True) #rename Sample column to Ch1

            # merge original csv with new pivot table
            merged_data = pd.concat([df, pv_table], axis=1, join_axes=[df.index])
            merged_data.to_csv(fullfilepath)




    if outputfile == None:
        foo = None
        return 0  # this is needed to communicate the completion status of this process to the outside world
        # 0, process not complete, file not chosen...

    else:
        #writeShortCSV(outputfile, fnames_keep)
        addPivotTableToCSV(outputfile, GUI_input)
        statusOut = ' Done!  Output file: ' + root + '_MOD.csv'
        statusColor = 'darkgreen'
        return statusOut, statusColor
        # means the process is complete, the external GUI is able to report "Done" status writing in green color


if __name__ == "__main__":
    main(inputfile,GUI_input)











