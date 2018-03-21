from random import seed, sample
from pprint import pprint
from bitarray import BitArray

class BloomFilter:

    def __init__(self, iterable=(), population=56, probes=6):
        self.population = xrange(population)
        self.probes = probes
        self.data = BitArray(population)
        for name in iterable:
            self.add(name)

    def add(self, name):
        seed(name)
        lucky = sample(self.population, k=self.probes)
        for i in lucky:
            self.data[i] = 1

    def __contains__(self, name):
        seed(name)
        lucky = sample(self.population, k=self.probes)
        return all(self.data[i] for i in lucky)

if __name__ == '__main__':

    hettingers = BloomFilter(['raymond', 'rachel', 'matthew', 'jackie', 'ramon', 'dennis', 'sharon'])
    print 'susan' in hettingers
    print 'rachel' in hettingers

    starks = BloomFilter(['eddard', 'catelyn', 'robb', 'jon snow', 'sansa', 'arya', 'bran', 'rickon'], population=1000, probes=7)
    print 'arya' in starks
    print 'ramsey' in starks