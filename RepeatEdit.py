#! python

## This program takes a user input file of two columns
## e.g. 
## abc    1
## bcd    1
## cde    2

## It will add a specific character or string to the end of each string in the first column
## It will then add a string or character to the end of each string in the second column
## It will then search for all the same occurances in the second column and put the first column
## in alignment with this and add a command to the beginning.  So your final output will look like this:
## e.g.
## cat abc* bcd* > 1.txt
## cat cde* > 2.txt

## Data entry on command line should look like this to get the above result:
## python RepeatEdit.py input.txt * .txt cat output.txt

# RepeatEdit.py

# Import the necessary modules
import sys

# This function gets the necessary information from the command line
def getData():
	commands = sys.argv
	filename = commands[1]
	
	infile = open(filename, 'r')
	seqData = []
	IDs = []
	for line in infile:
		seqRead, sampleID = line.split("\t")
		seqData.append(seqRead)
		IDOnly = sampleID.strip('\n')
		IDs.append(IDOnly)
	infile.close()

	return seqData, IDs, commands
	
# This function adds an input character.  Used for two commands in the program.
def addCharacter(DataList, commands, argument):
	newList = []
	addC = commands[argument]
	
	for i in DataList:
		entry = "{0}{1}".format(i, addC)
		newList.append(entry)
		
	return newList
	
# This function makes a tuple for easier matching downstream
def makeTuple(dataSet1, dataSet2):
	combinedData = []
	for i in range(len(dataSet1)):
		combinedData.append((dataSet1[i], dataSet2[i]))
		
	return combinedData
	
# This function recombines entries in the first column and makes sure only one ID gets assigned
def mergeData(combinedData, dataSet2):
	CombinedSeq = []
	finalIDs = []
	
	for i in dataSet2:
		storedData = []
		for (sequence, id) in combinedData: 
			if i == id:
				storedData.append(sequence)
		# Groups of entries for each ID are the result 
		CombinedSeq.append(storedData) #tuple of varying sizes. Which is dependent on ID.
		finalIDs.append(i)
		
		# Once an ID has been read in make sure to update the dataset so it is not covered again
		dataSet2[:] = (value for value in dataSet2 if value != i)
	
	return CombinedSeq, finalIDs

# This function takes all the information and prints it to the user defined output file.
def createTable(dataSet1, dataSet2, commands, argument1, argument2):
	filename = commands[argument2]
	commandToAdd = commands[argument1]
	
	outfile = open(filename, 'w')
	y = 0 #track with IDs
	
	for line in dataSet1:
	
		totalL = len(line)
		x = 1 #track with specific sequence groups
		
		for i in line:
			if x == 1:
				print("{0} {1}".format(commandToAdd, i), end =' ', file = outfile)
			elif totalL != x:
				print("{0}".format(i), end =' ', file = outfile)
			elif totalL == x:
				sampleName = dataSet2[y]
				print(y) #print unique ID being printed to new file
				print("{0} > {1}".format(i, sampleName), end ='\n', file = outfile)
			
			x = x + 1
		y = y + 1

	
	outfile.close()

# This function executes the program
def main():
	seqData, IDs, commands = getData()
	newSeqData = addCharacter(seqData, commands, 2)
	combinedData = makeTuple(newSeqData, IDs)
	CombinedSeq, finalIDs = mergeData(combinedData, IDs)
	newFinalIDs = addCharacter(finalIDs, commands, 3)
	createTable(CombinedSeq, newFinalIDs, commands, 4, 5)

	
if __name__ == '__main__': main()