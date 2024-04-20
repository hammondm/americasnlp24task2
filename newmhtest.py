#add closest change logic

import csv,sys,editdistance
from spacy.pipeline._edit_tree_internals.edit_trees import EditTrees
from spacy.strings import StringStore

pfx = '/home/hammond/Desktop/americasnlp2024/' + \
	'ST2_EducationalMaterials/data/'

edit_trees = EditTrees(StringStore([]))

change_to_trees = {}

train_path = pfx + sys.argv[1]
dev_path = pfx + sys.argv[2]
dev_prediction_path = sys.argv[3]

tf = open(train_path,newline="",encoding="utf-8")
tcsv = csv.DictReader(tf,delimiter="\t")
for row in tcsv:
	tree = edit_trees.add(
		row["Source"],
		row["Target"]
	)
	change = row["Change"]

	if change not in change_to_trees:
		change_to_trees[change] = {}

	if tree in change_to_trees[change]:
		change_to_trees[change][tree] += 1
	else:
		change_to_trees[change][tree] = 1
		#print(edit_trees.tree_to_str(tree))
tf.close()

ifile = open(dev_path,newline="",encoding="utf-8")
icsv = csv.DictReader(ifile,delimiter="\t")

ofile = open(dev_prediction_path,"w",newline="",encoding="utf-8")

fieldnames = icsv.fieldnames
#fieldnames.append("Predicted Target")

ocsv = csv.DictWriter(ofile,fieldnames=fieldnames,delimiter="\t")
ocsv.writeheader()

notchange = 0
nopred = 0

for row in icsv:
	prediction = None
	change = row["Change"]
	#print(row["Source"])
	if change in change_to_trees:
		trees = change_to_trees[change]
		for tree in sorted(trees,key=lambda t: trees[t],reverse=True):
			prediction = edit_trees.apply(tree,row["Source"])
			if prediction: break
			#print(f'\t{prediction}')
	if prediction:
		#row["Predicted Target"] = prediction
		row["Target"] = prediction
	else:
		notchange += 1
		#rank changes by edit distance
		ed = {}
		for c in change_to_trees:
			if c != change:
				r = editdistance.distance(change,c)
				ed[c] = r
			bcall = sorted(
				ed.items(),
				#reverse=True,
				key=lambda x: x[1]
			)
		#go through the changes one by one
		for bcnext in bcall:
			bc = bcnext[0]
			#apply most similar change
			trees = change_to_trees[bc]
			for tree in sorted(
					trees,
					key=lambda t: trees[t],
					#reverse=True
			):
				prediction = edit_trees.apply(tree,row["Source"])
				if prediction: break
			if prediction:
				#row["Predicted Target"] = prediction
				row["Target"] = prediction
				break
		if not prediction:
			#row["Predicted Target"] = row["Source"]
			row["Target"] = row["Source"]
			nopred += 1
	ocsv.writerow(row)

print(f'no change: {notchange}')
print(f'no pred: {nopred}')

ifile.close()
ofile.close()

