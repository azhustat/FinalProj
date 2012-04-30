# STAT 215B, Spring 2012
# Final Project
# co-occurrence matrix

import codecs
import re
import sys
import itertools # for examining all possible (n, 2) combinations


print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# opens output file
try:
	fout = codecs.open("coocmat.txt", "w", "utf-8")
except IOError:
	print "coocmat.txt could not be opened"
	sys.exit(1)

# words with frequency >= 10 
fwl = codecs.open("selectedwords.txt", "r", "utf-8") 
wlist = []
for word in fwl.readlines():
	wlist.append( word.strip() )	 

nwl = len(wlist)	

# list to store the co-occurrence matrix (stacked by columns)
coocmat = [0] * (nwl * nwl)
# length: 756^2 = 571536	
	
###

# reads in input file
lines = fp.readlines()

# defines regular expression patterns
wordpat = re.compile('(.+)/[\w]{1,6}$', re.UNICODE)

# for-loop to process each line
for part in lines:
	out = part.strip()
	out = out.split()	
	current = [''] * len(out)	

	for j in range(len(out)): 
		match = wordpat.findall(out[j].strip())	
		if (len(match) > 0): # there are empty lines due to reposting
			current[j] = match[0]
		
	inter = list(set(current).intersection(wlist))
	# examines all possible pairs
	for pair in itertools.combinations(inter, 2):
		k1 = wlist.index(pair[0])
		k2 = wlist.index(pair[1])
		coocmat[k1 + k2 * nwl] = coocmat[k1 + k2 * nwl] + 1
		coocmat[k2 + k1 * nwl] = coocmat[k1 + k2 * nwl]
	
		
###
# output
for i in range(nwl):
	s = ''	
	for j in range(nwl):
		s = s + str(coocmat[i + j * nwl]) + ' '
		
	print >> fout, s


###
fp.close()
fout.close()
fwl.close()	