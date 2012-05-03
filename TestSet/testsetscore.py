# STAT 215B, Spring 2012
# Final Project
# sentiment score assignment

import codecs
import re
import sys

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# opens output file
try:
	fout = codecs.open("testsetscore.txt", "w", "utf-8")
except IOError:
	print "testsetscore.txt could not be opened"
	sys.exit(1)
	
print >> fout, 'score postive negative negation hhc hhp hhn fc fp fn'
	
# reads in negation words
fnw = codecs.open("../data/negation.txt", "r", "utf-8")
nw = fnw.readlines()
nwset = set([ nw[0].strip() ])
for j in range(1, len(nw)):
	nwset.add( nw[j].strip() )
	
# reads in positive emotion words
fpem = codecs.open("../data/pos_emotion.txt", "r", "utf-8")
pem = fpem.readlines()
pemset = set([ pem[0].strip() ])
for j in range(1, len(pem)):
	pemset.add( pem[j].strip() )

# reads in positive evaluation words
fpev = codecs.open("../data/pos_eval.txt", "r", "utf-8")
pev = fpev.readlines()
pevset = set([ pev[0].strip() ])
for j in range(1, len(pev)):
	pevset.add( pev[j].strip() )

# reads in negative emotion words
fnem = codecs.open("../data/neg_emotion.txt", "r", "utf-8")
nem = fnem.readlines()
nemset = set([ nem[0].strip() ])
for j in range(1, len(nem)):
	nemset.add( nem[j].strip() )

# reads in negative evaluation words
fnev = codecs.open("../data/neg_eval.txt", "r", "utf-8")
nev = fnev.readlines()
nevset = set([ nev[0].strip() ])
for j in range(1, len(nev)):
	nevset.add( nev[j].strip() )

###

# finds the number of positive and negative words within 3-word window 
# of the given person
def checkPN(record, who):
	pn = [0] * 2
	for j in range(len(record)):
		if (record[j] == who):
			for m in range(-3, 0):
				if (j + m >= 0):
					if (record[j + m] == 'p'):
						pn[0] = pn[0] + 1
					elif (record[j + m] == 'n'):
						pn[1] = pn[1] + 1
			for m in range(1, 4):
				if (j + m < len(record)):
					if (record[j + m] == 'p'):
						pn[0] = pn[0] + 1
					elif (record[j + m] == 'n'):
						pn[1] = pn[1] + 1
	return(pn)			

							
## 
# topic-related names
hanhan = u'\u97e9\u5bd2'
fang = u'\u65b9\u821f\u5b50'

###

# reads in input file
lines = fp.readlines()

# defines regular expression patterns
wordpat = re.compile('(.+)/[\w]{1,6}$', re.UNICODE)

# for-loop to process each line
for part in lines:
	out = part.strip()
	out = out.split()	
	prethree = ['', '', ''] # keeps track of previous three words
	k = 0	
	# vec: score postive negative negation hhc hhp hhn fc fp fn
	vec = [0] * 10
	record = [''] * len(out)		
	for j in range(len(out)): 
		match = wordpat.findall(out[j].strip())
		if (len(match) > 0): # there are empty lines due to reposting
			word = match[0]
		
			# sentiment scores
			delta = 0
			if ((word in pemset) or (word in pevset)):
				delta = 1
				record[j] = 'p' # positive
				vec[1] = vec[1] + 1
			elif ((word in nemset) or (word in nevset)):
				delta = -1 	
				record[j] = 'n' # negative
				vec[2] = vec[2] + 1
			elif (word in nwset):
				record[j] = 'g' # negation word
				vec[3] = vec[3] + 1
			elif (word == hanhan):
				record[j] = 'h' # HanHan
				vec[4] = vec[4] + 1
			elif (word == fang):
				record[j] = 'f' # FangZhouzi
				vec[7] = vec[7] + 1	
		
			if (len(nwset.intersection(set(prethree))) == 1):
				delta = delta * (-1) 
		
			vec[0] = vec[0] + delta
			prethree[k] = word
		else:
			prethree[k] = ''
	
		k = k + 1
		if (k > 2):
			k = 0				
		
	if (vec[4] > 0):
		vec[5:7] = checkPN(record, 'h')
	if (vec[7] > 0):
		vec[8:10] = checkPN(record, 'f')		

	# output
	s = ''	
	for l in range(len(vec)):
		s = s + str(vec[l]) + ' '
			
	print >> fout, s


		

###
fp.close()
fout.close()
fpem.close()
fpev.close()
fnem.close()
fnev.close()
	