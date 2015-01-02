# Daniel Rodgers-Pryor, 16/8/2013

###
# I had to build my own bloom filter because the ones I could find used C code that wouldn't compile in windows.
###

from bitarray import bitarray
from sklearn.utils import murmurhash3_32
from math import log, ceil, floor

base_hash = lambda x: murmurhash3_32(x, seed = 0) # Note: might return a negative int
# If you don't have scikit.learn feel free to comment this out and add your
# own hash function here; just make sure that it has appropriate uniformity and speed.
# The fnv hash would be another good choice

class BloomFilter:
    def __init__(self, iterable = (), max_entries = None, false_positive_rate = 0.01):
        '''
            If max_entries is undefined, then iterable must be amenable to len() (and must be reconsumable).
            If this approach is taken, no objects should be added later (if they are, the false_positive_rate will no
            longer apply). If you wish to add objects later, specify a suitable max_entries value.
        '''
        if not max_entries: max_entries = len(iterable)
        max_entries = max(max_entries, 2) # Length 0 or 1 filters are pointless (length 0 filters break some of the maths)
        
        lg_2 = log(2)
        self.n = max_entries
        self.p = false_positive_rate
        optimal_size = -self.n * log(self.p) / (lg_2**2) # Formula from wikipedia
        self.index_bits = int(ceil(log(optimal_size, 2))) # Number of bits needed to address an array of this size
        self.m = 2**self.index_bits # Round up array size to a power of 2
        self.k = int(ceil((self.m * lg_2) / self.n))

        # Create and initialise bit-array:
        self.array = bitarray(self.m)
        self.array.setall(False)

        self.update(iterable)

    def capacity(self):
        return int(floor(-self.m * (log(2)**2) / log(self.p)))

    def hashes(self, key):
        '''
            Output will be an iterator of ints in [0, m)
            
            See A. Kirsch, M Mitzenmacher 'Less Hashing, Same Performance' for details on this fast, uniform hash set
        '''
        h1 = base_hash(key)
        h2 = base_hash(h1)
        return (abs(h1 + i*h2) % self.m for i in xrange(self.k))

    def append(self, key):
        for i in self.hashes(key):
            self.array[i] = 1

    def __contains__(self, key):
        return all(self.array[i] for i in self.hashes(key))
        
    def update(self, iterable):
        for i in iterable:
            self.append(i)

if __name__ == '__main__': # Module Tests
    b = BloomFilter(range(100))
    
    print 'All contained values return true:', all((i in b) for i in xrange(0, 100))
    print 'False positive rate:', sum((1 if (i in b) else 0) for i in xrange(10000, 20000))/float(10000)
        
    print 'Plotting historam of hashes to show uniformity...'
    import matplotlib.pyplot as plt
    a = sum((list(b.hashes(i)) for i in xrange(10000)), [])
    plt.hist(a, normed = True, bins = 100, range = (0, 1000))
    plt.show()
