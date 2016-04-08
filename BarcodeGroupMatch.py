#! python

# A quick program that matches the asssigns the group based on the barcode sequence when the barcode is stored in
# the fastq file as part of the findex or rindex but not on the sequence itself.
# It will create a group file and if the barcode is not found then it will assign a group name of "none"
# to the sequence.
# Proper usage is as follows:
	# python BarcodeGroupMatch.py <sequenceAndBarcodeFile> <oligoFile> <outputfilename>


# Load the needed modules for the program
import sys

# Read in a Command arguments for files to match
# Input other instructions from here 
def commandLine():
	commands = sys.argv
	inputfile = commands[1]
	oligofile = commands[2]
	outputfile = commands[3]
	
	return inputfile, oligofile, outputfile

# Reads in the data and creates a dictionary
def createDataArray(inputfile, n):
	inputfile = open(inputfile, 'r')
	
	SeqBarDict = {}
	if n == 'name':
		for line in inputfile:
			name, barcode = line.split('\t')
			barcodeStrip = barcode.strip('\n')
			SeqBarDict[name] = barcodeStrip
			
	if n == 'oligo':
		for line in inputfile:
			name, barcode, group = line.split('\t')
			groupStrip = group.strip('\n')
			SeqBarDict[barcode] = groupStrip
	
	inputfile.close()
			
	return SeqBarDict

# Create function to find matches and if it does not match add a none to it
def matchData(SeqBarDict, BarGroupDict):
	matchedDict = {}
	x = 1
	for i in SeqBarDict:
		print("sequence", x)
		try:
			bartoMatch = SeqBarDict[i]
			foundGroup = BarGroupDict[bartoMatch]
			matchedDict[i] = foundGroup
		except KeyError:
			matchedDict[i] = 'none'
		x = x + 1	
	return matchedDict

#Print out group file 
def makeGroupfile(matchedDict, outputfile):
	outfile = open(outputfile, 'w')
	for i in matchedDict:
		group = matchedDict[i]
		print("{0}\t{1}".format(i, group), end ='\n', file = outfile)
	
	outfile.close()
	
# Run the Program
def main():

	inputfile, oligofile, outputfile = commandLine()
	SeqBarDict = createDataArray(inputfile, "name")
	BarGroupDict = createDataArray(oligofile, "oligo")
	matchedDict = matchData(SeqBarDict, BarGroupDict)
	makeGroupfile(matchedDict, outputfile)

if __name__ == '__main__': main()