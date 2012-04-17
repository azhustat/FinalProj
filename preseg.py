# STAT 215B, Spring 2012
# Final Project
# pre-segmentation processing

import codecs
import re
import sys

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")
# emotion symbols
fes = codecs.open("./data/emotionSymbols.txt", "r", "utf-8")

try:
	fout = codecs.open("preseg.txt", "w", "utf-8")
except IOError:
	print "preseg.txt could not be opened"
	sys.exit(1)

try:
	finfo = codecs.open("info.txt", "w", "utf-8")
except IOError:
	print "info.txt could not be opened"
	sys.exit(1)
	
# constructs the emotion symbols
es = fes.readlines()
esdict = {}
for emotion in es:
	emotion = emotion.strip() # removes leading and trailing whitespace
	out = emotion.split("|")
	esdict[out[0]] = out[1]	
	
eskeys = esdict.keys()

# reads in input file
lines = fp.readlines()

# defines the regular expression patterns used in the for-loop
infopat = re.compile('^([0-9]+[\s][-0-9]+[\s][:0-9]+)[\s]', re.UNICODE)
urlpat = re.compile('(http://t.cn/[\w]+)', re.UNICODE)
menpat = re.compile('(@.+?)[\s:]', re.UNICODE) # [\s] includes '\n'

# for-loop to process each line
for part in lines:
	out = part
	# saves user ID and time stamp into info.txt
	outinfo = infopat.findall(out)[0]
	print >> finfo, outinfo
	out = infopat.sub('$', out)
	
	# multiple reposting
	reposting = re.findall("(.*?[^:])//@", out)
	if (len(reposting) > 0 ):
		out = reposting[0]
		
	# removes URLS		
	out = urlpat.sub(' ', out)	
	
	# substitute emotional symbols to words
	for emotion in eskeys:
		epat = re.compile(emotion, re.UNICODE)
		out = epat.sub('[' + esdict[emotion] + ']', out)
		#print emotion + ' ' + esdict[emotion]
		#print out + '\n'
	# mentions
	out = menpat.sub('@ ', out)
	out = out.strip() # removes leading and trailing whitespace
	print >> fout, out

fout.close()	
fp.close()	