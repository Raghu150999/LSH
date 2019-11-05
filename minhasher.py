import numpy as np

class MinHasher:

    def __init__(self, n, d, shingler):
        '''
        n: number of hash functions
        m: number of shingles
        sig: signature matrix
        d: number of documents
        '''
        self.shingler = shingler
        m = len(shingler.cm)
        self.m = m
        self.n = n
        self.d = d
        self.hasher = Hasher(n, m)
        # Here m is same as Infinity since all hash values are going to be less than m
        self.sig = np.full(shape=(n, d), fill_value=m)

        # Compute the signature matrix 
        for j, s in enumerate(self.shingler.cm):
            for docid in self.shingler.cm[s]:
                for i in range(n):
                    h = self.hasher.hash(i, j)
                    self.sig[i][docid] = min(self.sig[i][docid], h)

class Hasher:

    def __init__(self, n, m):
        '''
        Generates array of hash functions of the form a * x + b
        n: number of hash functions
        m: number of shingles
        '''
        self.a = np.random.randint(1, 100, n, dtype=int)
        self.b = np.random.randint(1, 100, n, dtype=int)
        self.m = m		
    
    def hash(self, i, x):
        '''
        Returns hash of x using the ith hash function
        '''
        return (self.a[i] * x + self.b[i]) % self.m