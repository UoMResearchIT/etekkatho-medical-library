#!/usr/bin/env python

# Imports
import sys
import os
import gzip
import xml.etree.ElementTree as ET
import urllib.request

# Main class
class XMLPDF():
	'Convert compress XML files into PDF articles'
	
	# Vars
	rootdir = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/toprocess/"
	output = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/output/"
	csvpath = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/csv/metadata.csv"
	
	def __init__(self):
		if os.path.exists(self.csvpath):
			os.remove(self.csvpath)
		
		self.processFiles()
	
	def processFiles(self):
		print('Processing files...')
		
		# Loop through files
		for subdir, dirs, files in os.walk(self.rootdir):
			for file in files:
				# Decompress file
				if file.endswith('.gz'):
					filepath = os.path.join(subdir, file)
					print('Unzipping: ', file)
					with gzip.open(filepath, 'rb') as f:
						file_content = f.read()
    					
						# Parse XML
						root = ET.fromstring(file_content)
						for child in root:
							singleFile = 'PMC'+child[0][1][0].text+'.pdf'
							singleName = 'PMC'+child[0][1][0].text
							
							'''
								↓ TODO: THIS BIT SHOULD BE MULTITHREADED ↓ 
							'''
							
							self.saveFile(singleName, singleFile, child)
								
	def saveFile(self, singleName, singleFile, child):
		# Download and save PDF
		response = urllib.request.urlretrieve('http://europepmc.org/backend/ptpmcrender.fcgi?accid='+singleName+'&blobtype=pdf', self.output+singleFile)
		
		# Save metadata to CSV file
		# First check the metadata exists, add it if it does
		
		'''
			↓  TODO: ERROR HANDLING FOR NON-EXISTENT NODES / DATA ↓ 
		'''
		
		issnppub = ''
		issnepub = ''
		pubname = ''
		publoc = ''
		
		try:
			issnppub = child[0][0][2].text
		except IndexError:
			issnppub = 'n/a'
		
		try:
			issnepub = child[0][0][3].text
		except IndexError:
			issnepub = 'n/a'
		
		try:
			pubname = child[0][0][4][0].text
		except IndexError:
			pubname = 'n/a'
		
		try:
			publoc = child[0][0][4][1].text
		except IndexError:
			publoc = 'n/a'
			
		try:
			firstAuthor = child[0][1][5][0][0][0].text
		except IndexError:
			firstAuthor = 'n/a'
		
		'''
			↓  TODO: COMPLETE THE FULL LIST OF JOURNAL AND ARTICLE METADATA. SWITCH TO DOM PARSING FROM ARRAY KEYS ↓ 
		'''
		
		metadata = {
			'filename': singleName,
			'journal-id-type': child[0][0][0].attrib['journal-id-type'],
			'journal-id': child[0][0][0].text,
			'type': child.attrib['article-type'],
			'journal-title': child[0][0][1].text,
			'issn-ppub': issnppub,
			'issn-epub': issnepub,
			'publisher-name': pubname,
			'publisher-location': publoc,
			'article-id': child[0][1][0].text,
			'article-title': child[0][1][4][0].text,
			'first-author': firstAuthor
		}
		self.updateCSV(metadata)
	
	def updateCSV(self, metadata):
		# Write the data to the CSV file. This will be used to populate a database
		print(metadata)
		
		outfile = open(self.csvpath, 'a')
		csvLine = ''
		for key, value in metadata.items():
			if value:
				csvLine += '"'+value+'", '
			else:
				csvLine += '"", '
			
		csvLine += '\n'
		outfile.write(csvLine)
    	

XMLPDF()
