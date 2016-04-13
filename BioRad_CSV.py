#!/usr/bin/env python 
import os
import sys
import csv

# comment the following line if using GUI
print "Enter full filepath of BioRad csv file"
inputfile = raw_input("> ")

# fieldnames to keep (MARK's samples)
fnames_keep = ['Well', 'Sample', 'Target', 'CopiesPer20uLWell']


# ----------------
def getOutputFileName(inputfile):
    # create output filename with same root and path as input file, adding the suffix _MOD


    # error checking
    if not os.path.isfile(inputfile):
        print 'That is not a valid file!'
        sys.exit(1) #gracefully exit Python
    else:
        print 'File exists!'
        # parse fullefilepath
        path, filename = os.path.split(inputfile)
        root, ext = os.path.splitext(filename)

        # fullfilepath for outputfile
        outputfile = path + '/' + root +'_MOD.csv'
        print outputfile
        return outputfile


# -------------
def writeShortCSV(inputfile,fnames_keep):

    outputfile = getOutputFileName(inputfile)
    print outputfile

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

def addPivotTableToCSV(fullfilepath):

    df = pd.read_csv(fullfilepath) # load as a dataframe

    # get file parts for outputfile
    #path, filename = os.path.split(fullfilepath)
    #root, ext = os.path.splitext(filename)

    # fullfilepath for outputfile
    #outputfile = path + '/' + root + '_MOD2.csv'


    # find duplicates in data
    dupl = df.duplicated(['Sample','Target'])
    dupl_indx = dupl[(dupl == 1)].index.tolist()

    #print('length of dupl_ind = ' + str(len(dupl_indx)))


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
    #print pv_table

    # merge original csv with new pivot table
    # first need to reset index of pv_table...
    pv_table = pv_table.reset_index()
    #print pv_table

    merged_data = pd.concat([df,pv_table], axis=1, join_axes=[df.index])

    merged_data.to_csv(fullfilepath)




                  
addPivotTableToCSV(modifiedFile)
    










# def main():
#     if len(sys.argv) != 3:
#         print 'usage: ./BioRad_CSV.py {--liver | --TBD} file'
#         sys.exit(1)
# 
#     option = sys.argv[1]
#     outputfilename = sys.argv[2]
#     filename = sys.argv[3]
#     
#     babynames = extract_names(filename)
#       
#     if option == '--summaryfile':
#         with open(outputfilename, 'w+') as f: #open file
#             f.write(str(babynames) + '\n')
#     else:
#         print babynames
# 
# 
# 
# if __name__ == '__main__':
#   main()