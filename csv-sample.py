#!/usr/bin/env python

from itertools import islice

csvpath = "/Users/zzalsrd5/Dropbox (eTekkatho)/eTekkatho Team Folder/PubMed and Healthcare/data/metadata/metadata.csv"

with open(csvpath) as myfile:
    head = list(islice(myfile, 1000))
    
    # Write the data to the CSV file
    outfile = open('metadata-sample.csv', 'a')
    
    for row in head:
        outfile.write(row)
    
    outfile.close()
    
    