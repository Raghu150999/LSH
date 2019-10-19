# LSH
Locality Sensitive Hashing (LSH) Algorithm is used to find similarity scores between documents.
Also known as near neighbour search. LSH uses repeated hashing to put similar documents in same bucket. Since, now the buckets have very less number of documents we can perform $O(N^2)$ similarity search if needed to find the most similar documents or we can find similarity of a given document with other documents by directly considering only those documents which lie in the same bucket as the given document.

# Libraries required:
- nltk
- numpy

Install the above requirements using pip.

# Usage
Ensure that the input document (document to find similarity) is in the corpus directory, and then run the following:
<pre><code>python3 main.py [filename]</code></pre>

# Example
<pre><code>python3 main.py test.txt</code></pre>