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
	fout = codecs.open("score.txt", "w", "utf-8")
except IOError:
	print "score.txt could not be opened"
	sys.exit(1)
	
# reads in negation words
fnw = codecs.open("./data/negation.txt", "r", "utf-8")
nw = fnw.readlines()
nwset = set([ nw[0].strip() ])
for j in range(1, len(nw)):
	nwset.add( nw[j].strip() )
	
# reads in positive emotion words
fpem = codecs.open("./data/pos_emotion.txt", "r", "utf-8")
pem = fpem.readlines()
pemset = set([ pem[0].strip() ])
for j in range(1, len(pem)):
	pemset.add( pem[j].strip() )

# reads in positive evaluation words
fpev = codecs.open("./data/pos_eval.txt", "r", "utf-8")
pev = fpev.readlines()
pevset = set([ pev[0].strip() ])
for j in range(1, len(pev)):
	pevset.add( pev[j].strip() )

# reads in negative emotion words
fnem = codecs.open("./data/neg_emotion.txt", "r", "utf-8")
nem = fnem.readlines()
nemset = set([ nem[0].strip() ])
for j in range(1, len(nem)):
	nemset.add( nem[j].strip() )

# reads in negative evaluation words
fnev = codecs.open("./data/neg_eval.txt", "r", "utf-8")
nev = fnev.readlines()
nevset = set([ nev[0].strip() ])
for j in range(1, len(nev)):
	nevset.add( nev[j].strip() )

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
	score = 0		
	for j in range(len(out)): 
		match = wordpat.findall(out[j].strip())
		if (len(match) > 0): # there are empty lines due to reposting
			word = match[0]
			if ((word in pemset) or (word in pevset)):
				delta = 1
			elif ((word in nemset) or (word in nevset)):
				delta = -1 	
			else:
				delta = 0
		
			if (len(nwset.intersection(set(prethree))) == 1):
				delta = delta * (-1) 
		
			score = score + delta
			prethree[k] = word
		else:
			prethree[k] = ''
		
		k = k + 1
		if (k > 2):
			k = 0				
		
	print >> fout, score


###
fp.close()
fout.close()
fpem.close()
fpev.close()
fnem.close()
fnev.close()
	