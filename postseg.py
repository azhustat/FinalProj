# STAT 215B, Spring 2012
# Final Project

import codecs
import re
import sys

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

try:
	fout = codecs.open("postseg.txt", "w", "utf-8")
except IOError:
	print "preseg.txt could not be opened"
	sys.exit(1)

lines = fp.readlines()
for part in lines:
	out = part.split()
	for j in range(len(out)): 
		z = out[j]
		wxpat = re.compile('(.+/[wx]$)', re.UNICODE)	
		out[j] = wxpat.sub(' ', z)
	out = ' '.join(out)
	out = out.strip() # removes leading and trailing whitespace
	print >> fout, out

fout.close()	
fp.close()