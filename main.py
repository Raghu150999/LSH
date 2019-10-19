import numpy
import os
from shingler import Shingler
from document import Document, DocumentCollection
from minhasher import MinHasher
from lsh import LSH

if __name__ == '__main__':
	files = os.listdir('corpus')
	files.sort()

	# 9 -> shingle size
	shingler = Shingler(9)

	# Document Collection
	dc = DocumentCollection()

	for i, filename in enumerate(files):
		with open('corpus/' + filename, encoding='utf8', errors='ignore') as f:
			raw = f.read()
			shingler.add(raw, i)
			document = Document(i, filename)
			dc.insert_document(document)

	# Perform Min Hashing
	# 100 -> number of hash functions
	minhasher = MinHasher(100, dc.cnt, shingler)

	# Perform LSH
	# 20 -> number of bands
	lsh = LSH(20, minhasher, dc)

	try:
		# Take filename as argument
		input_docname = str(sys.argv[1])
	except:
		input_docname = 'test.txt'

	sim_docs = lsh.get_similar(input_docname)
	for sim, docname in sim_docs:
		print('Document Name: ' + str(docname), 'Similarity: ' + str(sim))


