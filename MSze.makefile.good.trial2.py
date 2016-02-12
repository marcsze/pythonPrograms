import os
import sys
import glob
import csv

#Choose if there is anything part of the name you want to delete
delete = input('Type what to delete from the names or hit enter: ')

#generate list of fastq files in directory with R1
R1 = glob.glob('*R1*.fastq')
R1[:] = [s.replace(delete, '') for s in R1]

#generate list of fastq files in directory with R2
R2 = glob.glob('*R2*.fastq') 
R2[:] = [s.replace(delete, '') for s in R2]

#create list with only the group names and decide  whether to keep duplicates seperate

duplicate = input('Do you want to seperate duplicates?[Y/N] ')

if duplicate == 'Y':
	name = [i.split('_S', 1)[0] for i in R1] 
	from collections import Counter 
	counts = Counter(name) 
	for s,num in counts.items():
		if num > 1: 
			name[name.index(s)] = s + 'rep' + str(num)

if duplicate == 'N':
	name = [i.split('_S', 1)[0] for i in R1]

		
#Combine everything together into a single .csv file
title = input('Name your .file file: ')+'.file'

with open(title, 'w', newline='') as outfile:
		overall = csv.writer(outfile, delimiter = '\t')
		overall.writerows(zip(name, R1, R2))
	
quit()
