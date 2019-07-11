import pandas as pd
import sys

def newdump(filepath, newfile):
    """
    CLEAN DATA DUMP
    function to get rid of "ITEM: " in the header
    """
    f = open(filepath, 'rt')
    new = open(newfile, 'w')
    #make a list of each line from the file (each item of list is a string)
    lines = f.readlines()
    for i in range(len(lines)):
        #get rid of "ITEM:" anywhere that it appears
        lines[i] = lines[i].replace('ITEM: ', '')
        lines[i] = lines[i].replace('ATOMS ', '')
        new.write(lines[i])
    return        


def readin(filename, header):
    """
    function to read in dump file
    n denotes line in dump file where header for data begins
    """
    #stores output with space separated values as a df
    dat = pd.read_csv(filename, sep='\s+', header = header)
    #need to add in some analysis or cleaning
    return dat


def main():
    args = sys.argv
    n = int(args[3])
    newdump(args[1], args[2])
    dat = readin(args[2], n)
    print('This is the df you made: \n')
    print(dat)

#main()



#this executable needs three arguments
#the first is the filename of the original data dump
#the second is the new filename for the cleaned data
#the third (n) is the row of the header for our data within the cleaned data
