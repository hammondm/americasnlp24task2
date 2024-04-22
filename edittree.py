import re

#get all substrings
def getsubstrings(w):
	res = [w[i:j] for i in range(len(w))
			for j in range(i + 1,len(w) + 1)]
	return set(res)

#make one edit tree
def maketree(word1,word2):
	#all substrings of first word
	r1 = getsubstrings(word1)
	#all substrings of second word
	r2 = getsubstrings(word2)
	#shared substrings
	inter = r1.intersection(r2)
	#get the longest one
	res = sorted(
		list(inter),
		key=lambda x: len(x),
		reverse=True
	)
	#if no shared substrings, we're done
	#if len(res) == 0:
	if len(res) < 2:
		return (word1,word2)
	else:
		res = res[0]
		m1 = re.search(re.escape(res),word1)
		start1,end1 = m1.span()
		m2 = re.search(re.escape(res),word2)
		start2,end2 = m2.span()
		left = maketree(word1[:start1],word2[:start2])
		right = maketree(word1[end1:],word2[end2:])
		res = [left,(start1,end1),right]
	return res

#convert tree to regex
def converttoregex(y):
	if type(y) == list:
		res = ('','')
		for daughter in y:
			r1,r2 = converttoregex(daughter)
			res = (res[0] + str(r1),res[1] + str(r2))

	#force this to match anything this length or shorter
	elif type(y[0]) == int and type(y[1]) == int:
		dist = y[1] - y[0]
		res = ('(.{1,' + str(dist) + '})','\\xxx')
	elif y == ('',''):
		res = ('','')
	else:
		res = y
	return res

#make backreferences for regex
def makenums(s):
	c = 1
	m = re.search('\\\\xxx',s)
	while m:
		start,end = m.span()
		s = s[:start] + '\\' + str(c) + s[end:]
		m = re.search('\\\\xxx',s)
		c += 1
	return s

#make tree and rule
def makerule(word1,word2):
	x = maketree(word1,word2)
	inp,outp = converttoregex(x)
	outp = makenums(outp)
	return (inp,outp)

def applyrule(iw,ow,w):
	return re.sub(iw,ow,w)

