#!/usr/bin/env python

# Imports
import sys
import os
import gzip
import xml.etree.ElementTree as ET

# Main class
class XMLPDF():
	'Convert compress xml files into PDF articles'
	
	# Vars
	#rootdir = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/oa/SectionisedData/v.12.2013/"
	rootdir = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/toprocess/"
	output = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/output/"
	csvpath = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/csv/"
	
	def __init__(self):
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
							print(child.attrib['article-type'])
							
							# Save as PDF
							
								
							# Save id, title and other metadata to CSV file
							metadata = {
								'id': 
								'type': child.attrib['article-type']
							}
							self.updateCSV(metadata)
	
	def updateCSV(self, metadata):
		pass
	

XMLPDF()
