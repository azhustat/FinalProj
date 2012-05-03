# STAT 215B, Spring 2012
# Final Project
# post-segmentation processing

import codecs
import re
import sys
import copy

print sys.argv
filename = sys.argv[1] # input filename
fp = codecs.open(filename, "r", "utf-8")

# opens output file
try:
	fout = codecs.open("testsetpostseg.txt", "w", "utf-8")
except IOError:
	print "testsetpostseg.txt could not be opened"
	sys.exit(1)
	
# reads in stopping words
fsw = codecs.open("../data/stoppingwords.txt", "r", "utf-8")
sw = fsw.readlines()
swset = set([sw[0].strip()])
for j in range(1, len(sw)):
	swset.add(sw[j].strip())
	

# reads in conjunction words
fcon = codecs.open("../data/conjunction.txt", "r", "utf-8")
con = fcon.readlines()
although = []
but = []	
for i in range(0, 4):
	although.append(con[i].strip())
for i in range(4, 14):
	but.append(con[i].strip())	

####

# constructs dictionary using input record vector
def getConDict(rec):
	condict = {}
	k = 2
	while (k < len(rec)):
		for j in range(1, rec[k] + 1):
			condict[rec[k + j]] = rec[k - 1]
		k = k + rec[k] + 2
	return(condict)

# processes "Although (phrase 1), but (phrase 2)"
def processAB(s, aindex, bindex):
	mypat = re.compile('(^.*' + although[aindex] + '/[a-z]+.+?/w[kd][a-z]*).+' + but[bindex], re.UNICODE)
	if (len(mypat.findall(s)) > 0):
		return(mypat.findall(s)[0])
	else:
		return('')	

# processes "Although (phrase 1), (phrase 2)"		
def processA(s, aindex):
	mypat = re.compile('(^.*' + although[aindex] + '/[a-z]+.+?/w[kd][a-z]*)', re.UNICODE)
	if (len(mypat.findall(s)) > 0):
		return(mypat.findall(s)[0])
	else:
		return('')

# processes "(phrase 1), but (phrase 2)"
def processB(s, bindex):
	mypat = re.compile('(^.+?/w[kd][a-z]*).+' + but[bindex], re.UNICODE)
	if (len(mypat.findall(s)) > 0):
		return(mypat.findall(s)[0])
	else:
		return('')

###
# reads in input file
lines = fp.readlines()

# incorrect HanHan name tagging pattern
hanhan = u'\u97e9\u5bd2'
ichanpat = re.compile('(' + hanhan[0] + '/[a-z]{1,5}[\s]+' + hanhan[1] + '/[a-z]{1,5})', re.UNICODE)
hanpat = re.compile('(' + hanhan + '/[a-z]{1,5})', re.UNICODE)

# for-loop to process each line
for part in lines:
	out = part.strip()
	
	# handles the incorrect tagging of HanHan's name
	out = hanpat.sub(hanhan + '/nrh', out)
	out = ichanpat.sub(hanhan + '/nrh', out)
	
	# keeps track of conjunction words
	arec = [0]
	brec = [0] 

	# applies conjunction rules
	for i in range(len(although)):
		apat = re.compile('[\s]' + although[i] + '/[a-z]', re.UNICODE)
		match = apat.findall(out)
		# 'although' may be the first word of the sentence
		apat = re.compile('^' + although[i] + '/[a-z]', re.UNICODE)
		match2 = apat.findall(out)
		if (len(match) + len(match2) > 0):
			arec[0] = 1
			arec.append(i)
			arec.append(len(match) + len(match2))
			vec = []
			k = 0
			subs = out.split(although[i])
			for j in range(len(match) + len(match2)):
				arec.append(k + len(subs[j]))
				k = k + len(subs[j]) + len(although[i])

	for i in range(len(but)):
		bpat = re.compile('[\s]' + but[i] + '/[a-z]', re.UNICODE)
		match = bpat.findall(out)
		if (len(match) > 0):
			brec[0] = 1
			brec.append(i)
			brec.append(len(match))
			vec = []
			k = 0
			subs = out.split(but[i])
			for j in range(len(match)):
				brec.append(k + len(subs[j]))
				k = k + len(subs[j]) + len(but[i])	

	# constructs dictionaries for although and but
	if (arec[0]):
		adict = getConDict(arec)
		akeys = adict.keys()
		akeys.sort() # in-place sorting

	if (brec[0]):
		bdict = getConDict(brec)		
		bkeys = bdict.keys()
		bkeys.sort() # in-place sorting

	if (arec[0] + brec[0] > 0):
		endpat = re.compile('(.+?)[\s]./w[jvts]', re.UNICODE)
		subs = endpat.findall(out)
		endrec = []
		k = 0
		if (len(subs) > 0):
			for j in range(len(subs)):
				endrec.append(k + len(subs[j]))
				k = k + len(subs[j]) + 5
			if (endrec[len(endrec)-1] + 5 < len(out)):
				endrec.append(len(out) - 1)
		else:
			endrec.append(len(out) - 1)

		spt = [0, 0]
		record = []
		apt = 0
		bpt = 0
		for j in range(len(endrec)):
			ai = -1
			bi = -1
			spt = [spt[1], endrec[j]]
			if (arec[0]):
				if (apt < len(akeys) and akeys[apt] < spt[1]):
					ai = apt
					apt = apt + 1
			if (brec[0]):
				if (bpt < len(bkeys) and bkeys[bpt] < spt[1]):
					bi = bpt
					bpt = bpt + 1
			if (ai != -1 or bi != -1):
				record.append([spt[0], spt[1], ai, bi])
		
		#print part
		phrases = []
		for j in range(len(record)):
			ai = record[j][2]
			bi = record[j][3]
			#print str(j) + ' ' + out[(record[j][0]):(record[j][1])]
			if (ai != -1 and bi != -1):
				toadd = processAB(out[(record[j][0]):(record[j][1])], adict[akeys[ai]], bdict[bkeys[bi]])
			elif (ai != -1):
				toadd = processA(out[(record[j][0]):(record[j][1])], adict[akeys[ai]])
			else:
				toadd = processB(out[(record[j][0]):(record[j][1])], bdict[bkeys[bi]]) 
				
			if (len(toadd) > 0):
				phrases.append( toadd )	
				
		for j in range(len(phrases)):
			out = out.replace(phrases[j], ' ')			
	# end of applying conjunction rules
			
	out = out.split()				
	for j in range(len(out)): 
		z = out[j].strip()
		# removes certain lexical types (see README)
		wxpat = re.compile('(.+/[pueyoxw][\w]{0,5}$)', re.UNICODE)	
		out[j] = wxpat.sub(' ', z)
		# removes stopping words and number strings
		stempat = re.compile('(.+)/[\w]{1,6}$', re.UNICODE)
		npat = re.compile('([0-9]+)', re.UNICODE)
		match = stempat.findall(out[j])
		if (len(match) > 0):
			if (match[0] in swset or len(npat.findall(match[0])) > 0):
				out[j] = ''			
		
			
	out = ' '.join(out)
	out = out.strip() # removes leading and trailing whitespace	
	
	print >> fout, out

fout.close()	
fp.close()
fcon.close()
fsw.close()