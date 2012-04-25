# STAT 215B, Spring 2012
# Final Project
# conditional occurrence matrix

import codecs
import re
import sys


print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# opens output file
try:
	fout = codecs.open("condmat.txt", "w", "utf-8")
except IOError:
	print "condmat.txt could not be opened"
	sys.exit(1)

# words with frequency >= 10 
fwl = codecs.open("selectedwords.txt", "r", "utf-8") 
wlist = []
for word in fwl.readlines():
	wlist.append( word.strip() )	 

nwl = len(wlist)	

# sample tags
categories = [-1, 0, 1, 9]
fst = codecs.open("sampletags.txt", "r", "utf-8")
tlist = []
for tag in fst.readlines():
	tlist.append( int(tag.strip()) )


# list to store the conditional occurrence matrix (stacked by columns)
condmat = [0] * (nwl * 4)
	
###

# reads in input file
lines = fp.readlines()

# defines regular expression patterns
wordpat = re.compile('(.+)/[\w]{1,6}$', re.UNICODE)

# for-loop to process each line
for i in range(len(lines)):
	out = lines[i].strip()
	out = out.split()	
	current = [''] * len(out)	

	for j in range(len(out)): 
		match = wordpat.findall(out[j].strip())	
		if (len(match) > 0): # there are empty lines due to reposting
			current[j] = match[0]
	
	k2 = categories.index( tlist[i] )		
	for word in set(current).intersection(wlist):
		k1 = wlist.index(word)
		condmat[k1 + k2 * nwl] = condmat[k1 + k2 * nwl] + 1
	
		
###
# output
for i in range(nwl):
	s = ''	
	for j in range(4):
		s = s + str(condmat[i + j * nwl]) + ' '
		
	print >> fout, s


###
fp.close()
fout.close()
fwl.close()
fst.close()