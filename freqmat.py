# STAT 215B, Spring 2012
# Final Project
# frequency matrix

import codecs
import re
import sys


print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# opens output file
try:
	fout = codecs.open("freqmat.txt", "w", "utf-8")
except IOError:
	print "freqmat.txt could not be opened"
	sys.exit(1)

# words with frequency >= 10 
fwl = codecs.open("selectedwords.txt", "r", "utf-8") 
wlist = []
for word in fwl.readlines():
	wlist.append( word.strip() )	 

nwl = len(wlist)


# list to store the frequency matrix (stacked by columns)
freqmat = [0] * (len(wlist) * 3000)

	
###

# reads in input file
lines = fp.readlines()

# defines regular expression patterns
wordpat = re.compile('(.+)/[\w]{1,6}$', re.UNICODE)

# for-loop to process each line
for i in range(len(lines)):
	out = lines[i].strip()
	out = out.split()

	for j in range(len(out)): 
		match = wordpat.findall(out[j].strip())	
		if (len(match) > 0): # there are empty lines due to reposting
			word = match[0]
			if (word in wlist):
				k = wlist.index(word)
				freqmat[k + i * nwl] = freqmat[k + i * nwl] + 1

		
###
# output
for i in range(nwl):
	s = ''	
	for j in range(len(lines)):
		s = s + str(freqmat[i + j * nwl]) + ' '
		
	print >> fout, s


###
fp.close()
fout.close()
fwl.close()