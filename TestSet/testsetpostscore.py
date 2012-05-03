# STAT 215B, Spring 2012
# Final Project
# post-score-assignment processing

import codecs
import re
import sys

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# opens output file
try:
	fout = codecs.open("testsetpostscore.txt", "w", "utf-8")
except IOError:
	print "testsetpostscore.txt could not be opened"
	sys.exit(1)
	
# reads in negation words
fnw = codecs.open("../data/negation.txt", "r", "utf-8")
nw = fnw.readlines()
nwset = set([ nw[0].strip() ])
for j in range(1, len(nw)):
	nwset.add( nw[j].strip() )	
	
# reads in degree words
fdw = codecs.open("../data/degree.txt", "r", "utf-8")
dw = fdw.readlines()
dwset = set([ dw[0].strip() ])
for j in range(1, len(dw)):
	dwset.add( dw[j].strip() )


# for word counts dictionary
worddict = {}

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
			if ((word in nwset) or (word in dwset)):
				out[j] = ''
			else:
				# constructs word counts dictionary
				worddict[word] = worddict.get(word, 0) + 1	

	out = ' '.join(out)
	out = out.strip() # removes leading and trailing whitespace	

	print >> fout, out

###

# writes word counts into a file
try:
	fwc = codecs.open("testsetwords.txt", "w", "utf-8")
except IOError:
	print "testsetwords.txt could not be opened"
	sys.exit(1)

for word in worddict.keys():
	print >> fwc, word + ' ' + str(worddict[word])

###
fout.close()	
fp.close()
fnw.close()
fwc.close()	