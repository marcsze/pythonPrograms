#! python

#TaxaAnalysis.py
## Version 1.1
## This program takes a taxonomy file, a shared file, level of classification, and output file 
## on the command line.  One current limitation is that the number of OTUs in the shared file 
## and the taxonomy file must match.  The other problem is that at the moment there is no 
## relative abundance option and only the total reads are returned.  I will work on this for 
## later iterations.  The program returns a tab text file that can be viewed in excel, etc.

## Examples of the command line entry:
## python TaxaAnalysis.py test.taxonomy test.shared 2 uneven=y taxa=True y output.txt
## python TaxaAnalysis.py test.taxonomy test.shared 6 uneven=y taxa=False n output.txt

## For this program the tax levels are as follows:
## 1 = Domain
## 2 = Phylum
## 3 = Class
## 4 = Order
## 5 = Family
## 6 = Genus

## For this program you can output relative abundance or total reads.
## using y in the command line will create a relative abundance table.
## using n in the command line will create a total read count table.


#################### Need to create unequal files ability.

# Load the needed modules for the program
import sys, re


# need to use sys to get command line input can do len(sys.argv) and str(sys.argv)
# also have to use re to get the regex library
# get argument from command line
def commandLine():
	commands = sys.argv
	taxFile = commands[1]
	sharedFile = commands[2]
	taxLevel = commands[3]
	uneven = commands[4]
	taxaPrint = commands[5]
	RelAbund = commands[6]
	outputFile = commands[7]
		
	return taxFile, taxLevel, sharedFile, uneven, taxaPrint, RelAbund, outputFile


# use argument to read in file and seperate out each respective taxonomy component 
# with header stored seperate
def seperateTaxFile(taxa):
	infile = open(taxa, 'r')
	x = 0
	header = []
	OTU = []
	total = []
	taxonomy = []
	for line in infile:
		if x == 0:
			for i in line.split("\t"):
				header.append(i)
		else:	
			OTUs, totals, taxonomies = line.split("\t")
			unit = OTUs.strip('\n')
			
			OTU.append(unit)
			total.append(totals)
			taxonomy.append(taxonomies)
		
		x = x + 1
		
	infile.close()
	
	return header, OTU, total, taxonomy

	
def equalizeData(taxonomy, OTU, shared):
	taxaFile = {}
	NewTaxonomy = []
	NewOTU = []
	OTUList = []
	x = 0
	for i in OTU:
		taxaFile[i] = taxonomy[x]
		x = x + 1
		
	x = 0
		
	infile = open(shared, 'r')
	for line in infile:
		for i in line.split("\t"):
			if x == 0:
				unit = i.strip('\n')
				OTUList.append(unit)
				
		x = x + 1			
	infile.close()
	
	for j in OTU:
		for k in OTUList:
			if j == k:
				NewTaxonomy.append(taxaFile[j])
				NewOTU.append(j)
	
	return NewTaxonomy, NewOTU
			
			
# Use split to seperate into taxonomic groups
def splitTaxonomy(taxonomy, taxLevel):
	# Create list file to hold tax classifications
	domain = []
	phylum = []
	BClass = []
	BOrder = []
	family = []
	genus = []
	
	for line in taxonomy:
		x = 1
		for i in line.split(";"):
			if x == 1:
				domain.append(i)
			elif x == 2:
				phylum.append(i)
			elif x == 3:
				BClass.append(i)
			elif x == 4:
				BOrder.append(i)
			elif x == 5:
				family.append(i)
			elif x == 6:
				genus.append(i)
			x = x + 1
			
	# Generate the table to return based on user defined original input
	taxSelection = eval(taxLevel)
	
	if taxSelection == 1:
		return domain
	elif taxSelection == 2:	
		return phylum
	elif taxSelection == 3:
		return BClass
	elif taxSelection == 4:
		return BOrder
	elif taxSelection == 5:
		return family
	if taxSelection == 6:
		return genus
	
# regex to only take the characters
def removeNumbers(result):
	table = []
	characterRegex = re.compile(r'''\w+''', re.VERBOSE)
	for i in result:
		mo = characterRegex.search(i)
		table.append(mo.group())
	
	return table


# need to recombine all the components back together 
def taxaKey(OTU, table):
	tableKey = []
	for i in range(len(table)):
		tableKey.append((OTU[i], table[i]))
		
	return tableKey


# output a file as named by user (Only does taxonomy file, unused function at the moment)
# Want to make this as an option in the workflow entry
def createOutput(header, OTU, total, table):
		temptable = []
		outfile = open("taxonomyKey.txt", 'w')
		x = 0
		
		for i in range(len(table)):
			if x == 0:
				print("{0}\t{1}\t{2}".format(header[0], header[1], header[2]), end ='', file = outfile)
				print("{0}\t{1}\t{2}".format(OTU[i], total[i], table[i]), end ='\n', file = outfile)	
			elif x > 0 and x < len(table):
				print("{0}\t{1}\t{2}".format(OTU[i], total[i], table[i]), end ='\n', file = outfile)		
			elif x == len(table):
				print("{0}\t{1}\t{2}".format(OTU[i], total[i], table[i]), end ='', file = outfile)		

			
			x = x + 1

		outfile.close()

# A function to generate a list of all groups in the user defined taxonomic level
def generateUniqueTax(table):
	uniqueTable = []
	for i in table:
		if i in uniqueTable:
			uniqueTable = uniqueTable
		else:
			uniqueTable.append(i)
			
	return uniqueTable

	
# A function to generate a list of all the individual sample names in the inputed data set	
def generateGroupInfo(shared):
	infile = open(shared, 'r')
	sampleNames = []
	x = 0
	
	for line in infile:
		
		if x > 0:
			y = 0
			for k in line.split("\t"):
				if y == 1:
					sampleNames.append(k)
				else:
					sampleNames = sampleNames
					
				y = y + 1	
		
		x = x + 1
		
	infile.close()
	return sampleNames
	
	
	
# A function to add all those that match a specific group for every individual in the data set	
# Like to use a dictionary here instead of lists
	# Needs sample name as the key and taxonomic level group, and totals as values 
def generateTotals(uniqueTable, table, sampleNames, shared):
	infile = open(shared, 'r')
	otuHeader = []
	finalData = {}
	x = 0
	
	for line in infile:
		if x == 0:
			for i in line.split("\t"):
				otuHeader.append(i)
		else:	
			tempNumbers = []
			y = 0
			for k in line.split("\t"):
				if y <= 2:
					tempNumbers = tempNumbers
				else:
					tempNumbers.append(k)
				y = y + 1
			
			taxaData = {}
			
			for i in uniqueTable:
				total = 0
				for j in range(len(table)):
					if i == table[j]:
						total = total + eval(tempNumbers[j])
				taxaData[i] = total
			
			#Before Reset Need to add all of the data to a file to be parsed later 	
			finalData[sampleNames[x-1]] = taxaData
			
		x = x + 1
	
	infile.close()
	
	return finalData


# This function creates the total counts to generate the relative abundance table
def totalCounts(finalData, sampleNames, uniqueTable):
	countsTable = {}
	
	for i in sampleNames:
		test = finalData[i]
		x = 0
		for j in uniqueTable:
			tempValue = test[j]
			x = x + tempValue
		
		countsTable[i] = x
		
	return countsTable


# This function generates the relative abundance table
def relativeAbundance(finalData, countsTable, uniqueTable, sampleNames):
	
	for i in sampleNames:
		total = countsTable[i]
		tempdata = finalData[i]
		
		for j in uniqueTable:
			counts = tempdata[j]
			relabund = (counts/total)*100
			tempdata[j] = relabund
			
		finalData[i] = tempdata
			
	return finalData

#Print to file
def createDataTable(finalData, sampleNames, uniqueTable, final):
	outfile = open(final, 'w')
	
	x = 0
	
	for i in sampleNames:
		if x == 0:
			for j in range(len(uniqueTable)):
				if j == 0:
					print("{0}".format("SampleIDs"), end ='\t', file = outfile)
					print("{0}".format(uniqueTable[j]), end ='\t', file = outfile)
				elif j < len(uniqueTable)-1:
					print("{0}".format(uniqueTable[j]), end ='\t', file = outfile)
				elif j == len(uniqueTable)-1:
					print("{0}".format(uniqueTable[j]), end='\n', file = outfile)
			
			tempData = finalData[i]
			
			for k in range(len(uniqueTable)):
				if k == 0:
					print("{0}".format(i), end ='\t', file = outfile)
					print("{0}".format(tempData[uniqueTable[k]]), end ='\t', file = outfile)
				elif k < len(uniqueTable)-1:
					print("{0}".format(tempData[uniqueTable[k]]), end ='\t', file = outfile)
				elif k == len(uniqueTable)-1:
					print("{0}".format(tempData[uniqueTable[k]]), end ='\n', file = outfile)
		else:
			tempData = finalData[i]
			for k in range(len(uniqueTable)):
				if k == 0:
					print("{0}".format(i), end ='\t', file = outfile)
					print("{0}".format(tempData[uniqueTable[k]]), end ='\t', file = outfile)				
				elif k < len(uniqueTable)-1:
					print("{0}".format(tempData[uniqueTable[k]]), end ='\t', file = outfile)
				elif k == len(uniqueTable)-1:
					print("{0}".format(tempData[uniqueTable[k]]), end ='\n', file = outfile)
	
		x = x + 1
	
	outfile.close()

# Run the program
def main():
	taxa, taxLevel, shared, uneven, taxaPrint, RelAbund, final = commandLine()
	header, OTU, total, taxonomy = seperateTaxFile(taxa)
	
	if uneven[7] in "Yy":
		taxonomy, OTU = equalizeData(taxonomy, OTU, shared)
	
	result = splitTaxonomy(taxonomy, taxLevel)
	table = removeNumbers(result)
	
	if taxaPrint[5] in "Tt":
		createOutput(header, OTU, total, table)
		
	test = taxaKey(OTU, table)
	uniqueTable = generateUniqueTax(table)
	sampleNames = generateGroupInfo(shared)
	
	finalData = generateTotals(uniqueTable, table, sampleNames, shared)
	
	# This controls whether a relative abundance or total count table is used
	if RelAbund[0] in 'yY':
		countsTable = totalCounts(finalData, sampleNames, uniqueTable)
		relabund = relativeAbundance(finalData, countsTable, uniqueTable, sampleNames)
		createDataTable(relabund, sampleNames, uniqueTable, final)
	else:
		createDataTable(finalData, sampleNames, uniqueTable, final)
	
	
	
	
	
	
	
	
	
	
	








if __name__ == '__main__': main()






