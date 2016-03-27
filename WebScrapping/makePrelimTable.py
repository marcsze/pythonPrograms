#! Python

def getInput(datafile):
	links = open(datafile, 'r')
	dataTable = []
	for line in links:
		goodLine = line.strip('\n')
		dataTable.append(goodLine)

	links.close()
	
	return dataTable


def createOutput(dataTable):
	finalTable = {}
	namesfile = []
	x = 1
		
	for i, data in enumerate(dataTable):
		temppoint = []
			
		if x%2 == 0:
			for point in data.split("_"):
				pointGood = point.strip('\n')
				temppoint.append(pointGood)
			finalTable[dataTable[i-1]] = temppoint
					
		x = x + 1
			
			
	outfile = open("test.txt", 'w')		
	
	for j in finalTable:
		data2 = finalTable[j]
		print("{0}\t".format(j), end ='', file = outfile)
		
		for k, jobInfo in enumerate(data2):
			if k != len(data2) - 1:
				print("{0}\t".format(jobInfo), end ='', file = outfile)
			else:
				print("{0}".format(jobInfo), end ='\n', file = outfile)
			

	outfile.close()


def main():

	dataTable = getInput("editedOuput2.txt")
	createOutput(dataTable)


if __name__ == '__main__': main()