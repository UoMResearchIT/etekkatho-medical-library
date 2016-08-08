#!/usr/bin/env python

# Imports
import sys
import os
import gzip
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
from multiprocessing.pool import ThreadPool as Pool
import time
import csv

# Main class
class XMLPDF():
	'Generate a CSV file of metadata for 1.4 million medical articles, and download the corresponding PDFs'
	
	# Vars
	rootdir = "/media/zzalsrd5/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/toprocess/"
	output = "/media/zzalsrd5/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/output/"
	csvpath = "/media/zzalsrd5/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/csv/metadata.csv"
	errorpath = "/media/zzalsrd5/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/errors/errors.txt"
	lastxmlfile = "/media/zzalsrd5/Seagate Backup Plus Drive/uom/et_pubmed/europepmc.org/ftp/state/lastxml.txt"
	
	def __init__(self, task):
		if task == 'process':
			if os.path.exists(self.csvpath):
				# First remove the old file
				os.remove(self.csvpath)
				
				# Create a new one with the header line
				outfile = open(self.csvpath, 'w')
				outfile.write('pmcid,filename,journal-id-type,journal-id,article-type,journal-title,issn-ppub,issn-epub,publisher-name,publisher-location,article-title,authors,affiliation\n')
				outfile.close()
			
			self.processFiles()
			
		elif task == 'download':
			self.downloadPDFs()
		else:
			print('No task specified, exiting...')
	
	#@profile
	def processFiles(self):
		print('Processing files...')
		startTime = time.strftime("%c")
		print('Start time: ', time.strftime("%c"))
		
		pool_size = 1000
		pool = Pool(pool_size)
		
		# Loop through files
		for subdir, dirs, files in os.walk(self.rootdir):
			for file in files:
				# Read file
				if file.endswith('.xml'):
					filepath = os.path.join(subdir, file)
						
					for event, element in ET.iterparse(filepath):
						if element.tag == 'article':
							strainer = SoupStrainer('article')
							article = BeautifulSoup(ET.tostring(element), 'lxml', parse_only=strainer)
							pmcid = 'PMC'+article.find("article-id", {"pub-id-type" : "pmcid"}).getText()

							# Save the data, and use multiple threads
							try:
								pool.apply_async(self.saveData, (pmcid, article,))
							except ValueError:
								print('Restarting pool... (1)')
								pool = Pool(pool_size)
								pool.apply_async(self.saveData, (pmcid, article,))
							
							print('.', end="", flush=True)
							
							element.clear()
						
					# Fix for memory leak issue
					del element
					del article
						
					try:	
						pool.close()
						pool.join()
					except ValueError:
						print('Restarting pool... (2)')
						pool = Pool(pool_size)
						pool.close()
						pool.join()
						
		print('Processing finished: start {} end {}'.format(startTime, time.strftime("%c")))
								
	def saveData(self, pmcid, article):	
		# Get the metadata
		metadata = self.getMetadata(article, pmcid)
		
		# Save metadata to CSV file
		self.updateCSV(metadata)
	
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
				authors += author.text+','
				author.next_sibling	
				
		except AttributeError:
			authors = 'n/a'
		
		try:
			affiliation = ''
			
			for aff in article.findAll("aff"):
				affiliation += aff.text+','
				aff.next_sibling
				
		except AttributeError:
			affiliation = 'n/a'
		
		singleFile = pmcid+'.pdf'
		authors = authors.rstrip(',')
		affiliation = affiliation.rstrip(',')	
		
		metadata = [
			pmcid,
			singleFile,
			journalIDType,
			journalID,
			articleType,
			journalTitle,
			issnppub,
			issnepub,
			pubname,
			publoc,
			articleTitle,
			authors,
			affiliation
		]
		
		return metadata
	
	def updateCSV(self, metadata):
		# Write the data to the CSV file. This will be used to update the solr index	
		with open(self.csvpath, "a") as fp:
			wr = csv.writer(fp, dialect='excel', lineterminator = '\n')
			wr.writerow(metadata)
	
	def updateLastXML(self, filename):
		# Save the last opened XML file
		outfile = open(self.lastxmlfile, 'a')
		outfile.write(filename)
		outfile.close()
	
	def downloadPDFs(self):
		### Download all the files extracted from the metadata
		startTime = time.strftime("%c")
		# Loop through the CSV
		f = open(self.csvpath)
		metadata = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
		
		for row in metadata:
			pmcid = row[8]
			
			### Check the input is a PMC ID
			if 'PMC' in pmcid:
				print('Starting thread for: '+pmcid)
				
				pool = Pool(30)
				pool.apply_async(self.saveFile, (pmcid,))
				pool.close()
				pool.join()
			else:
				print('Something is wrong. '+pmcid+' is not a PMC id')
				sys.exit(0)
			
		f.close()
		
		print('Finished downloading all files: start {} end {}.'.format(startTime, time.strftime("%c")))
	
	def saveFile(self, pmcid):	
		# Check of the file already exists
		singleFile = pmcid+'.pdf'
		if os.path.isfile(self.output+singleFile):
			# File already downloaded
			print('Already got: '+singleFile)		
		else:
			# No file, download it
			print('Downloading: '+singleFile)	
			try:
				response = urllib.request.urlretrieve('http://europepmc.org/backend/ptpmcrender.fcgi?accid='+pmcid+'&blobtype=pdf', self.output+singleFile)
			except urllib.error.HTTPError:
				errorfile = open(self.errorpath, 'a')
				errorfile.write(pmcid+'\n')


XMLPDF('process')
