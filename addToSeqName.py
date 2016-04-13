#! python

# A small program to match either a fasta or qual file based on whether the barcode was found or not.
# Need a group file that designates sequences without a recognized barcode as "none".
# To use the program entries should look like the following:
	# python matchFastaGroup.py <fastaORqualFile> <groupFilew> <outputfileName.fasta> <thingToAdd>

	
# Need to add a component that incorporates new mapfile into the workflow
	
# Load the needed modules for the program
import sys, re


# Read in a Command arguments for files to match
# Input other instructions from here 
def commandLine():
	commands = sys.argv
	fastafile = commands[1]
	groupfile = commands[2]
	outputfile = commands[3]
	addition = commands[4]
	
	return fastafile, groupfile, outputfile, addition
	
	
# Read in data and create dictionary
def makeDataArray(inputfile, type):
	inputfile = open(inputfile, 'r')
	if type == "fasta":
		print("Reading in Fasta file.....")
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
	elif type == "group":
		print("Reading in group file......")
		DataDict = {}
		for line in inputfile:
			seqName, group = line.split('\t')
			DataDict[seqName] = group.strip('\n')
	# deal with data that is a map file
	else:
		DataDict = {}
		for line in inputfile:
			number, seqname = line.split('\t')
			DataDict[number] = seqname.strip('\n')
		
	return DataDict	
	
	
def makeNewFasta(fastaDict, addition, outputfile):
	outfile = open(outputfile, 'w')
	print("Creating new fasta file......")
	for i in fastaDict:
		sequence = fastaDict[i]
		print(">{0}_{1}\n{2}".format(i, addition, sequence), end ='\n', file = outfile)
		
	outfile.close()	
	
# Make a new group file based on the groups not labelled with "none"
def makeNewGroups(groupDict, addition, outputfile):
	NewOuputfile = re.sub('.fasta', '.groups', outputfile)
	outfile = open(NewOuputfile, 'w')
	print("Creating new group file.......")
	for i in groupDict:
		group = groupDict[i]
		print("{0}_{1}\t{2}".format(i, addition, group), end ='\n', file = outfile)
	
	outfile.close()	
	
	
# Run the actual program			
def main():
	fastafile, groupfile, outputfile, addition = commandLine()
	fastaDict = makeDataArray(fastafile, "fasta")
	groupDict = makeDataArray(groupfile, "group")
	makeNewFasta(fastaDict, addition, outputfile)
	makeNewGroups(groupDict, addition, outputfile)
	print("Complete")
	

if __name__ == '__main__': main()