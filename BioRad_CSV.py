#!/usr/bin/env python 
import os
import sys
import csv


print "Enter full filepath of folder containing BioRad csv file"
a_path = raw_input("> ")

# error checking
if os.path.exists(a_path):
    print "File exists!"
    #print('Path is %s, file is %s, filebasename is %s' % (path,filename,root))
else:
    print 'That is not a valid path!'
    sys.exit(1) #gracefully exit Python
      
# get file parts for outputfile
path, filename = os.path.split(a_path)
root, ext = os.path.splitext(filename)
    
# fieldnames to keep    
fnames_keep = ['Well','Sample','Target','CopiesPer20uLWell'] 

# fullfilepath for outputfile
outputfile = path + '/' + root +'_MOD.csv'
      
    
# -------------
def writeShortCSV(inputfile,outputfile,fnames_keep): 
    
    with open(outputfile,'w') as csvoutfile: # open output file
        writer = csv.DictWriter(csvoutfile,fieldnames=fnames_keep,extrasaction='ignore')
        writer.writeheader()

        with open(inputfile,'rU') as csvfile: # open input file
            reader = csv.DictReader(csvfile) # read csv file  
            # creates dict of the form:  {key, value} = {Column_header, value}
            
            for row in reader:   # iterate over rows, each row is a dict
                writer.writerow(row)

                
                # view key, value pairs in each dict / row
                #for k,v in row.items():
                    #print k,v

print('Modified CSV file saved as:  ' + outputfile)
# ------------------           

writeShortCSV(a_path,outputfile,fnames_keep)
    
    
    
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
   
modifiedFile = '/Users/lindanieman/Documents/WORK/MGH CC/Droplets/LIVER \
20160220 WTA SCALEUP PLATE 1 MK_MOD.csv'    

getUniqueValues(modifiedFile)




# --------------------------
import pandas as pd
import numpy as np

def addPivotTableToCSV(fullfilepath):

    df = pd.read_csv(fullfilepath) # load as a dataframe

    # get file parts for outputfile
    path, filename = os.path.split(fullfilepath)
    root, ext = os.path.splitext(filename)

    # fullfilepath for outputfile
    outputfile = path + '/' + root + '_MOD2.csv'


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

    merged_data.to_csv(outputfile)






                  
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