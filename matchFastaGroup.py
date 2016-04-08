#! python

# A small program to match either a fasta or qual file based on whether the barcode was found or not.
# Need a group file that designates sequences without a recognized barcode as "none".
# To use the program entries should look like the following:
	# python matchFastaGroup.py <fastaORqualFile> <groupFilewithNoneIncluded> <outputfileName>

# Load the needed modules for the program
import sys, re


# Read in a Command arguments for files to match
# Input other instructions from here 
def commandLine():
	commands = sys.argv
	fastafile = commands[1]
	groupfile = commands[2]
	outputfile = commands[3]
	
	return fastafile, groupfile, outputfile

# Read in data and create dictionary
def makeDataArray(inputfile, type):
	inputfile = open(inputfile, 'r')
	if type == "fasta":
		# Create specific environment variables
		x = 1
		names = []
		sequence = []
		DataDict = {}
		# Read data in and create a dictionary
		for line in inputfile:
			if x%2 != 0:
				newLine = re.sub('>', '', line)
				names.append(newLine.strip('\t\n'))
			else:
				sequence.append(line.strip('\n'))
			
			x = x + 1
			
		inputfile.close()
		
		for i, seqName in enumerate(names):
			DataDict[seqName] = sequence[i]
	# deal with data that is a group file
	else:
		DataDict = {}
		for line in inputfile:
			seqName, group = line.split('\t')
			DataDict[seqName] = group.strip('\n')
	
	return DataDict	
		
# Create a fasta file with only the groups not labelled with "none"
def makeNewFasta(fastaDict, groupDict, outputfile):
	outfile = open(outputfile, 'w')
	for i in fastaDict:
		sequence = fastaDict[i]
		group = groupDict[i]
		# If the group does not equal none then keep it and output it to a new file
		if group != "none":
			print("Adding Sequence", i)
			print(">{0}\n{1}".format(i, sequence), end ='\n', file = outfile)
		
	outfile.close()	
		

# Run the actual program			
def main():
	fastafile, groupfile, outputfile = commandLine()
	fastaDict = makeDataArray(fastafile, "fasta")
	groupDict = makeDataArray(groupfile, "groups")
	makeNewFasta(fastaDict, groupDict, outputfile)

if __name__ == '__main__': main()


