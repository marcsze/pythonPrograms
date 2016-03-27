#! Python

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests, re, time
# Might need to run the following command in windows to change the encoder 
# chcp 65001

def getInput(datafile):
	links = open(datafile, 'r')
	LinkStorage = []
	for line in links:
		goodLine = line.strip('\n')
		LinkStorage.append(goodLine)

	links.close()
	
	return LinkStorage

def createOutput(storedData, name):
	outfile = open(name, 'w')
	
	for i in storedData:
		descrip = storedData[i]
		print("{0}\n\t{1}".format(i, descrip), file = outfile)
	
	
	outfile.close()

def main():
	LinkStorage = getInput("combined.txt")
	storedData = {}
	linkedData = {}
	companyData = {}
	for i in LinkStorage:
		
		PosNameSearch = re.search('http://www.biospace.com/jobs/job-listing/(.*)-[0-9]', i)
		position = PosNameSearch.group(1)
		html = requests.get(i).text
		soup = BeautifulSoup(html, 'html5lib')
		description = soup.find("div").findAll("span", attrs={'id':'ctl00_phMainContent_lblJobRequirements'})
		company = soup.find("div").findAll("span", attrs={'id':'ctl00_phMainContent_lblJobDescription'})
		storedData[position] = description
		linkedData[position] = i
		companyData[position] = company
		print(i)
		time.sleep(1)
		
	createOutput(storedData, "output2.txt")
	createOutput(linkedData, "linkedData1.txt")
	createOutput(companyData, "companyData.txt")
	

if __name__ == '__main__': main()