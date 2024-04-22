#use my edit tree implementation

import sys,editdistance,edittree

#location of files
pfx = '/home/hammond/Desktop/americasnlp2024/' + \
	'ST2_EducationalMaterials/data/'

#get language name
lang = sys.argv[1]

#make filenames
trainfile = pfx + lang + '-train.tsv'
devfile = pfx + lang + '-dev.tsv'
outfile = lang + '.tsv'

#read training data
f = open(trainfile,'r')
t = f.read()
f.close()
#strip header and final empty line
t = t.split('\n')[1:-1]

#get edit trees
trees = {}
for line in t:
	#split the line into fields
	ID,source,change,target = line.split('\t')
	#get the rule
	rule = edittree.makerule(source,target)
	#keep track of each rule
	if change in trees:
		if rule in trees[change]:
			trees[change][rule] += 1
		else:
			trees[change][rule] = 1
	else:
		trees[change] = {}
		trees[change][rule] = 1

#for change in trees:
	#print(change)
	#for rule in trees[change]:
		#print(f'\t{trees[change][rule]}')
		#print(f'\t{rule}')

#read in dev data
g = open(devfile,'r')
t = g.read()
g.close()
#remove header and final empty line
t = t.split('\n')[:-1]
header = t[0]

#make output
h = open(outfile,'w')
#write header
h.write(f'{header}\tPredicted Target\n')
for line in t[1:]:
	#split test/dev file
	ID,source,change,target = line.split('\t')
	#check if we've seen the change
	#if not, find the most similar one
	#(if not, return the form unchanged)
	if change not in trees:
		ed = {}
		for c in trees:
			r = editdistance.distance(change,c)
			ed[c] = r
		bcall = sorted(
			ed.items(),
			key=lambda x: x[1]
		)
		bc = bcall[0][0]

	else:
		#get the rules for the change
		bc = change

	rules = trees[bc]
	#sort by frequency
	bestones = sorted(
		rules,
		key=lambda x: trees[bc][x],
		#key=lambda x: len(x),
		reverse=True
	)
	#go through the rules 1 by 1
	for best in bestones:
		res = edittree.applyrule(best[0],best[1],source)
		#stop when a rule does something
		if res != target: break
	h.write(f'{ID}\t{source}\t{change}\t{target}\t{res}\n')
h.close()

