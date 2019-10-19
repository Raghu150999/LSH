from nltk.tokenize import RegexpTokenizer

class Shingler:
	'''
	Performs shingling for the given document and adds it to the characteristic matrix
	'''
	def __init__(self, k):
		'''
		k: shingle size
		cm: characteristic matrix
		icm: inverted characteristic matrix
		'''
		self.k = k
		self.cm = {}
		self.icm = {}

	def preprocess(self, text_doc):
		# Remove punctuations
		tokenizer = RegexpTokenizer(r'\w+')
		tokens = tokenizer.tokenize(text_doc)

		# Convert to lower case
		for i, token in enumerate(tokens):
			tokens[i] = token.lower()

		return tokens

	def get_text(self, lis):
		processed_list = ['$']
		for term in lis:
			# string converted to list
			tmp = list(term)
			processed_list.extend(tmp)
			# adding '$' symbol to denote white space
			processed_list.append('$')
		return processed_list

	def add(self, text_doc, docid):
		'''
		Shingles the document and adds it to the characteristic matrix
		'''
		lis = self.preprocess(text_doc)
		text = self.get_text(lis)
		k = self.k
		i = k
		s = text[:k]
		l = len(text)
		self.insert(s, docid)
		while i < l:
			s = s[1:]
			s.append(text[i])
			self.insert(s, docid)
			i += 1
	
	def insert(self, s, docid):
		'''
		Inserts the docid in the set of shingle s
		'''
		s = tuple(s)
		if self.cm.get(s):
			self.cm[s].add(docid)
		else:
			self.cm[s] = {docid}
		if self.icm.get(docid):
			self.icm[docid].add(s)
		else:
			self.icm[docid] = {s}

	def jcsim(self, doc1, doc2):
		'''
		Finds the jacquard similarity between doc1 and doc2
		'''
		cnt11 = 0
		for s in self.icm[doc1]:
			if s in self.icm[doc2]:
				cnt11 += 1
		l1 = len(self.icm[doc1])
		l2 = len(self.icm[doc2])
		return (cnt11 / (l1 + l2 - cnt11))
		
			
