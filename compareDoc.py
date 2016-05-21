#! python

# New program to compare or find samples from two different files and output a 
# 3 columns of information on the data of samples that are in both files.  Uses 
# certain convertToList.py programs to edit the existing text file to make it more 
# amenable for downstream use.  The three columnas that are outputed are as follows 
# sequencingID, GroupID, file found in.  
# An example of how to use this program is below:

## python compareDoc.py samplesToMatch.txt "FD" sample.txt output.txt


# Read in necessary programs and functions
import sys
from convertToList import readData, identifySamples

# Read in a Command arguments for the program
# Input other instructions from here
def commandLine():
	commands = sys.argv
	textToConvert = commands[1]
	pattern = commands[2]
	mappingFile = commands[3]
	outputfile = commands[4]
	return textToConvert, pattern, mappingFile, outputfile

# Read in test data as a dictionary to modify file as needed
def readTestFile(mappingFile, pattern):
	data = open(mappingFile, 'r')
	testDict = {}
	x = 0
	for line in data:
		if x != 0:
			sampleID, barcode, linker, group = line.split("\t")
			if pattern in group:
				testDict[group.strip('\n')] = sampleID

		x = x + 1
	return testDict

# Make the comparison between the data and test data
def compareData(dataList, testDict):
	noMatchList = []
	YESMatchDict = {}
	for i, group in enumerate(dataList):
		try:
			sample = testDict[group]
			YESMatchDict[group] = sample
		except KeyError:
			noMatchList.append(group)
	return YESMatchDict, noMatchList
	
	
# This function will output a tab-delimited text file of the samples
def saveFindings(YESMatchDict, mappingFile, outputfile):
	#change to 'a' for appending to file rather than write (w)
	outfile = open(outputfile, 'a')
	for i in YESMatchDict:
		sample = YESMatchDict[i]
		print("{0}\t{1}\t{2}".format(sample, i, mappingFile), 
		end ='\n', file = outfile)
	outfile.close()

# Run the overall program
def main():
	textToConvert, pattern, mappingFile, outputfile  = commandLine()
	dataList = readData(textToConvert)
	goodData = identifySamples(dataList, pattern)
	testDict = readTestFile(mappingFile, pattern)
	YESMatchDict, noMatchList = compareData(dataList, testDict)
	saveFindings(YESMatchDict, mappingFile, outputfile)

if __name__ == '__main__': main()
