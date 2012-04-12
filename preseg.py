# STAT 215B, Spring 2012
# Final Project

import codecs
import re
import sys

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

try:
	fout = codecs.open("preseg.txt", "w", "utf-8")
except IOError:
	print "preseg.txt could not be opened"
	sys.exit(1)

lines = fp.readlines()
for part in lines:
	out = part
	# multiple reposting
	reposting = re.findall("(.+?[^:])//", part)
	if (len(reposting) > 0 ):
		out = reposting[0]
	# removes URLS
	urlpat = re.compile('(http://t.cn/[\w]+)[\s]', re.UNICODE)	
	out = urlpat.sub(' ', out)	
	# mentions
	menpat = re.compile('(@.+?)[\s:]', re.UNICODE)
	out = menpat.sub('@ ', out)
	out = out.strip() # removes leading and trailing whitespace
	print >> fout, out

fout.close()	
fp.close()	