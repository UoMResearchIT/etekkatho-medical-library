#!/usr/bin/env python

# Imports
import sys
import os
import gzip
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import urllib.request
from multiprocessing.pool import ThreadPool as Pool

# Main class
class XMLPDF():
	'Generate a CSV file of metadata for 1.4 million medical articles, and download the corresponding PDFs'
	
	# Vars
	rootdir = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/toprocess/"
	output = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/output/"
	csvpath = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/csv/metadata.csv"
	errorpath = "/volumes/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/errors/errors.txt"
	
	def __init__(self):
		if os.path.exists(self.csvpath):
			os.remove(self.csvpath)
			
		if os.path.exists(self.errorpath):
			os.remove(self.errorpath)
		
		self.processFiles()
	
	def processFiles(self):
		print('Processing files...')
		
		pool_size = 300
		pool = Pool(pool_size)
		i = 0
		
		# Loop through files
		for subdir, dirs, files in os.walk(self.rootdir):
			for file in files:
				# Read file
				if file.endswith('.xml'):
					filepath = os.path.join(subdir, file)
					
					with open(filepath, 'rb') as f:
						file_content = f.read()
    					
						# Parse XML
						root = ET.fromstring(file_content)
						for child in root:
							article = BeautifulSoup(ET.tostring(child), 'lxml')
							pmcid = 'PMC'+article.find("article-id", {"pub-id-type" : "pmcid"}).getText()
							
							#print('Parsing article ID: ', pmcid)
							i = i+1
							
							# Save the data, use multiple threads
							try:	
								pool.apply_async(self.saveFile, (pmcid, article, i,))
							except ValueError:
								print('Restarting pool... (1)')
								pool = Pool(pool_size)
								pool.apply_async(self.saveFile, (pmcid, article, i,))
						
						try:	
							pool.close()
							pool.join()
						except ValueError:
							print('Restarting pool... (2)')
							pool = Pool(pool_size)
							pool.close()
							pool.join()
								
	def saveFile(self, pmcid, article, i):
		# Download and save PDF
		singleFile = pmcid+'.pdf'
		
		try:
			response = urllib.request.urlretrieve('http://europepmc.org/backend/ptpmcrender.fcgi?accid='+pmcid+'&blobtype=pdf', self.output+singleFile)
		except urllib.error.HTTPError:
			errorfile = open(self.errorpath, 'a')
			errorfile.write(pmcid+'\n')	
			
		# Get the metadata
		metadata = self.getMetadata(article, pmcid)
		
		# Save metadata to CSV file
		self.updateCSV(metadata, i)
	
	def getMetadata(self, article, pmcid):
		try:
			issnppub = article.find("issn", {"pub-type" : "ppub"}).getText()
		except AttributeError:
			issnppub = 'n/a'
			
		try:
			issnepub = article.find("issn", {"pub-type" : "epub"}).getText()
		except AttributeError:
			issnepub = 'n/a'
		
		try:
			pubname = article.find("publisher-name").getText()
		except AttributeError:
			pubname = 'n/a'
			
		try:
			publoc = article.find("publisher-loc").getText()
		except AttributeError:
			publoc = 'n/a'	

		try:
			journalTitle = article.find("journal-title").getText()
		except AttributeError:
			journalTitle = 'n/a'	

		try:
			journalID = article.find("journal-id").getText()
		except AttributeError:
			journalID = 'n/a'
		
		try:
			jidt = article.find("journal-id", {"journal-id-type" : True})
			journalIDType = jidt["journal-id-type"]
		except AttributeError:
			jidt = 'n/a'
			
		try:
			artype = article.find("article", {"article-type" : True})
			articleType = artype["article-type"]
		except AttributeError:
			articleType = 'n/a'

		try:
			articleTitle = article.find("article-title").getText()
		except AttributeError:
			articleTitle = 'n/a'
		
		try:
			authors = ''
			
			for author in article.findAll("surname"):
				authors += author.text+', '
				author.next_sibling	
		except AttributeError:
			authors = 'n/a'
		
		try:
			affiliation = ''
			
			for aff in article.findAll("aff"):
				affiliation += aff.text+', '
				aff.next_sibling	
		except AttributeError:
			affiliation = 'n/a'
		
		singleFile = pmcid+'.pdf'
		
		metadata = {
			'pmcid': pmcid,
			'filename': singleFile,
			'journal-id-type': journalIDType,
			'journal-id': journalID,
			'article-type': articleType,
			'journal-title': journalTitle,
			'issn-ppub': issnppub,
			'issn-epub': issnepub,
			'publisher-name': pubname,
			'publisher-location': publoc,
			'article-title': articleTitle,
			'authors': authors,
			'affiliation': affiliation
		}
		
		return metadata
	
	def updateCSV(self, metadata, i):
		# Write the data to the CSV file. This will be used to populate a database
		print('Writing data for entry number:', i)
		
		outfile = open(self.csvpath, 'a')
		csvLine = ''
		for key, value in metadata.items():
			#print('Adding:', key, value)
			
			if value:
				csvLine += '"'+value+'", '
			else:
				csvLine += '"", '
			
		csvLine += '\n'
		outfile.write(csvLine)	

XMLPDF()
