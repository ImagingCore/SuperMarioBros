#!/usr/bin/env python 
import os
import sys
import csv

# comment the following line if using GUI
#print "Enter full filepath of BioRad csv file"
#inputfile = raw_input("> ")

inputfile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/Data/MEL DDPCR PLATE 1 APRIL-1-2016-NoBlanks.csv'
GUI_input = 'duplex'
modifiedFile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/Data/MEL DDPCR PLATE 1 APRIL-1-2016-NoBlanks_MOD.csv'


if GUI_input == 'singleplex':
    # fieldnames to keep (Singleplex samples)
    fnames_keep = ['Well', 'Sample', 'Target', 'CopiesPer20uLWell']
elif GUI_input == 'duplex':
    fnames_keep = ['Well', 'Sample', 'TargetType','Target', 'CopiesPer20uLWell']

# ----------------
def getOutputFileName(inputfile):
    # create output filename with same root and path as input file, adding the suffix _MOD


    # error checking
    if not os.path.isfile(inputfile):
        print 'That is not a valid file!'
        sys.exit(1) #gracefully exit Python
    else:
        #print 'File exists!'
        # parse fullefilepath
        path, filename = os.path.split(inputfile)
        root, ext = os.path.splitext(filename)

        # fullfilepath for outputfile
        outputfile = path + '/' + root +'_MOD.csv'
        #print outputfile
        return outputfile

# -------------
def writeShortCSV(inputfile,fnames_keep):

    outputfile = getOutputFileName(inputfile)
    #print outputfile

    with open(outputfile,'w') as csvoutfile: # open output file
        writer = csv.DictWriter(csvoutfile,fieldnames=fnames_keep,extrasaction='ignore')
        writer.writeheader()

        with open(inputfile,'rU') as csvfile: # open input file
            reader = csv.DictReader(csvfile) # read csv file  
            # creates dict of the form:  {key, value} = {Column_header, value}
            
            for row in reader:   # iterate over rows, each row is a dict
                writer.writerow(row)


#print('Modified CSV file saved as:  ' + outputfile)
# ------------------           

writeShortCSV(inputfile,fnames_keep)

# ------------------    
def getUniqueValues(fullfilepath):  
        
    with open(fullfilepath,'rU') as csvfile: # open input file
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
import pandas as pd

def addPivotTableToCSV(fullfilepath, GUI_input):

    df = pd.read_csv(fullfilepath) # load as a dataframe

    # get file parts for outputfile
    #path, filename = os.path.split(fullfilepath)
    #root, ext = os.path.splitext(filename)

    # fullfilepath for outputfile
    #outputfile = path + '/' + root + '_MOD2.csv'




    if GUI_input == 'singleplex':
        # find duplicates in data
        dupl = df.duplicated(['Sample','Target'])
        dupl_indx = dupl[(dupl == 1)].index.tolist()

        # rename single duplicate, alert user if there is more than one duplicate
        if len(dupl_indx) > 1:
            print 'Multiple duplicates found in data!'
            sys.exit(1)
        elif (len(dupl_indx) == 1):
            sampleName = df.loc[dupl_indx,'Sample']
            df.loc[dupl_indx,'Sample'] = sampleName + '-' + str(2)
            print('Duplicate renamed to: ' + df.loc[dupl_indx,'Sample'])

        # pivot table
        pv_table = df.pivot_table(index='Sample', columns='Target', values='CopiesPer20uLWell')

        # merge original csv with new pivot table
        # first need to reset index of pv_table...
        pv_table = pv_table.reset_index()

        merged_data = pd.concat([df, pv_table], axis=1, join_axes=[df.index])
        merged_data.to_csv(fullfilepath)

    elif GUI_input == 'duplex':
        # find duplicates in data
        dupl = df.duplicated(['Sample','TargetType','Target'])
        dupl_indx = dupl[(dupl == 1)].index.tolist()

        # rename single duplicate, alert user if there is more than one duplicate
        if len(dupl_indx) > 1:
            print 'Multiple duplicates found in data!'
            print dupl
            sys.exit(1)
        elif (len(dupl_indx) == 1):
            sampleName = df.loc[dupl_indx, 'Sample']
            df.loc[dupl_indx, 'Sample'] = sampleName + '-' + str(2)
            print('Duplicate renamed to: ' + df.loc[dupl_indx, 'Sample'])


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

                  
addPivotTableToCSV(modifiedFile,GUI_input)
    
print 'DONE!'







