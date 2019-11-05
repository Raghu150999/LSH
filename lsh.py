import numpy as np

class LSH:

    def __init__(self, b, minhasher, dc):
        '''
        Performs the Locality Sensitive Hashing using the signature matrix 
        which is the output of the MinHasher
        b: number of bands
        r: number of rows in each band
        condition br = n
        n: number of hash function (number of rows in the signature matrix)
        '''
        self.minhasher = minhasher
        n = minhasher.n
        assert(n % b == 0)
        r = n // b
        self.r = r
        self.b = b
        self.dc = dc
        # Number of documents in the corpus
        d = dc.cnt
        # Array of dictionaries, each dictionary is for each band which will hold buckets for hashed vectors in that band
        self.buckets = np.full(b, {})
        # Mapping from docid to h to find the buckets in which document with docid was hashed
        self.docth = np.zeros((d, b), dtype=int)
        for i in range(b):
            for j in range(d):
                low = int(i * r)
                high = int((i+1) * r)
                l = minhasher.sig[low:high, j]
                h = hash(tuple(l))
                if self.buckets[i].get(h):
                    self.buckets[i][h].append(j)
                else:
                    self.buckets[i][h] = [j]
                self.docth[j][i] = h
    
    def get_similar(self, dn):
        '''
        Returns documents similar to input document
        dn: document name
        '''
        if self.dc.dntid.get(dn) == None:
            raise KeyError('No document with the given name found in the corpus.')

        docid = self.dc.dntid[dn]
        # Collection of documents similar to docid, taking union of all buckets in which docid is present
        c = []
        for b, h in enumerate(self.docth[docid]):
            c.extend(self.buckets[b][h])
        c = set(c)
        # Similar documents
        sim_list = []
        for doc in c:
            if doc == docid:
                continue
            sim = self.minhasher.shingler.jcsim(docid, doc)
            sim_list.append((sim, self.dc.idtdn[doc]))
        sim_list.sort(reverse=True)
        return sim_list
