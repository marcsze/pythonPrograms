#! python

# A small program to match either a fasta or qual file based on whether the barcode was found or not.
# Need a group file that designates sequences without a recognized barcode as "none".
# To use the program entries should look like the following:
	# python matchFastaGroup.py <fastaORqualFile> <mapfile> <groupFilewithNoneIncluded> <outputfileName.fasta>

	
# Need to add a component that incorporates new mapfile into the workflow
	
# Load the needed modules for the program
import sys, re


# Read in a Command arguments for files to match
# Input other instructions from here 
def commandLine():
	commands = sys.argv
	fastafile = commands[1]
	mapfile = commands[2]
	groupfile = commands[3]
	outputfile = commands[4]
	
	return fastafile, mapfile, groupfile, outputfile

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
	elif type == "group":
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
		
# Create a fasta file with only the groups not labelled with "none"
def makeNewFasta(fastaDict, mapDict, groupDict, outputfile):
	outfile = open(outputfile, 'w')
	for i in fastaDict:
		sequence = fastaDict[i]
		seqName = mapDict[i]
		group = groupDict[seqName]
				
		# If the group does not equal none then keep it and output it to a new file
		if group != "none":
			print("Adding Sequence to fasta: ", i)
			print(">{0}_{1}\n{2}".format(i, group, sequence), end ='\n', file = outfile)
		
	outfile.close()	

# Make a new group file based on the groups not labelled with "none"
def makeNewGroups(fastaDict, mapDict, groupDict, outputfile):
	NewOuputfile = re.sub('.fasta', '.groups', outputfile)
	outfile = open(NewOuputfile, 'w')
	
	for i in fastaDict:
		sequence = fastaDict[i]
		seqName = mapDict[i]
		group = groupDict[seqName]
				
		# If the group does not equal none then keep it and output it to a new file
		if group != "none":
			print("Adding Sequence to Group: ", i)
			print("{0}_{1}\t{2}".format(i, group, group), end ='\n', file = outfile)
	
	outfile.close()

# Run the actual program			
def main():
	fastafile, mapfile, groupfile, outputfile = commandLine()
	fastaDict = makeDataArray(fastafile, "fasta")
	groupDict = makeDataArray(groupfile, "groups")
	mapDict = makeDataArray(mapfile, "map")
	makeNewFasta(fastaDict, mapDict, groupDict, outputfile)
	makeNewGroups(fastaDict, mapDict, groupDict, outputfile)
	

if __name__ == '__main__': main()


