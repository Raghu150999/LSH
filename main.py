import numpy
import os
from shingler import Shingler
from document import Document, DocumentCollection
from minhasher import MinHasher
from lsh import LSH
import math

def getbr(n, t):
	'''
	Function for parameter tuning
	n: number of hash functions
	t: threshold value of similarity required
	Returns the value of b which ensures (1/b)^(1/r) >= t
	It turns out that b * (1 / b) is a monotonically decreasing function for b >= 1
	Hence, we can use binary search to find the value of 'b' satisfying the above relation
	'''
	# n * log t
	nlt = n * math.log(t)
	low = 1
	high = n
	while low < high:
		# Candidate value for b
		mid = (low + high + 1) // 2
		val = - mid * math.log(mid)
		if val >= nlt:
			low = mid
		else:
			high = mid - 1
	r = n // low
	return low, r


if __name__ == '__main__':
	
	files = os.listdir('corpus')
	files.sort()

	# t: threshold
	t = 0.55

	# k: shingle length
	k = 4
	shingler = Shingler(k)

	# Document Collection
	dc = DocumentCollection()

	for i, filename in enumerate(files):
		with open('corpus/' + filename, encoding='utf8', errors='ignore') as f:
			raw = f.read()
			shingler.add(raw, i)
			document = Document(i, filename)
			dc.insert_document(document)

	# Perform Min Hashing
	# t: threshold value
	# n: number of hash functions
	n = 100
	b, r = getbr(n, t)
	# Recomputing so that b * r == n
	n = b * r
	minhasher = MinHasher(n, dc.cnt, shingler)

	# Perform LSH
	# b: number of bands
	lsh = LSH(b, minhasher, dc)

	try:
		# Take filename as argument
		input_docname = str(sys.argv[1])
	except:
		print('Usage: python main.py <filename>', 'Using default document test.txt')
		input_docname = 'test.txt'

	sim_docs = lsh.get_similar(input_docname)
	avgsim = 0
	for sim, docname in sim_docs:
		print('Document Name: ' + str(docname), 'Similarity: ' + str(sim))
		avgsim += sim
	if len(sim_docs) > 0:
		avgsim /= len(sim_docs)
		print('Average similarity: ', avgsim)
	else:
		print('No documents found!')
		


