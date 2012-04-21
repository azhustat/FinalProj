# STAT 215B, Spring 2012
# Final Project
# pre-tagging processing

import codecs
import re
import sys

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# output file
try:
	fout = codecs.open("hanhanweibo.txt", "w", "utf-8")
except IOError:
	print "hanhanweibo.txt could not be opened"
	sys.exit(1)

# no print-out of info
#try:
#	finfo = codecs.open("info.txt", "w", "utf-8")
#except IOError:
#	print "info.txt could not be opened"
#	sys.exit(1)

###

# reads in input file
lines = fp.readlines()

# defines the regular expression patterns used in the for-loop
infopat = re.compile('^([0-9]+[\s][-0-9]+[\s][:0-9]+)[\s]', re.UNICODE)
urlpat = re.compile('(http://t.cn/[\w]+)', re.UNICODE)

# data structure set to eliminate duplicates
messages = set([])

# for-loop to process each line
for part in lines:
	out = part
	# removes user ID and time stamp
	out = infopat.sub(' ', out)

	# multiple reposting
	reposting = re.findall("(.*?[^:])//@", out)
	if (len(reposting) > 0 ):
		out = reposting[0]
	
	# removes URLS		
	out = urlpat.sub(' ', out)
	
	if (out != ' '):
		# removes leading and trailing whitespace
		messages.add(out.strip())
		
###		
for out in messages:	
	print >> fout, out

fout.close()
fp.close()
