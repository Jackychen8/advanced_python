''' Goals:
* Learn to instrument (trace) Python w/ tracer objects.
* Practice subclassing builtin types.
* Review the dunder methods: cmp hash lt le gt ge eq ne
* Solidfy the containers presentation
* Refine understanding of hashability and immutability
* See the effects of the matching logic:
    if a is b: return True      # indentity implies equality
    if hash(a) != hash(b): return False
    return a == b

* dir shows methods of a class
__cmp__ is a thee-way compare: -1 means less-than   0 means equal   1 means greater-than
__lt__ __ge__ __le__ __gt__ __eq__ __ne__ -> boolean (or something else)

name = 'Jacky'
print(f'Hello {name}')

* The basic idea is that you can create a subclass that wraps inherited methods with
* parts that will print/log details about the methods being called for you

* #MeToo, Tracer Object Analogy
'''
from math import log
from bisect import bisect
from random import randrange


cmpcnt = 0
hashcnt = 0

def reset():
    global cmpcnt, hashcnt
    cmpcnt = 0
    hashcnt = 0

def show():
    print('{0} compares and {1} hashes'.format(cmpcnt, hashcnt))

class Int(int):
    'Tracer version of int()'

    def __cmp__(self, other):# other is standard for binary operations
        global cmpcnt
        cmpcnt += 1
        print('Comparing {0} + {1}'.format(self, other))

        # Method Resolution Order (MRO): cooperative multiple inheritance

        return int.__cmp__(self, other)
        #return super(Int, self).__cmp__(other) # awkward code and undeterministic

    def __hash__(self):
        global hashcnt
        hashcnt += 1
        print('Hash {0}'.format(self))
        return int.__hash__(self)

class B(int):
    pass

class C(Int, B):
    pass

# obj.__mro__ gives you the method resolution order which is priority where python looks
# when searching for method/characteristic

s = map(Int, [10, 20, 30, 40, 20, 5, 10, 15, 20])
a = Int(11)
b = Int(20)
c = s[2]
n = len(s)

def bigfunc(a, b):
    return 'happy' if a < b else 'sad'
# bigfunc(10, 5)
# bigfunc(Int(10), Int(5))


###########################################################
reset(); print a in s; show()
# O(n) linear search, left-to-right. If not found, takes len(s) compares.

reset(); print b in s; show() # Early-out for matches.
# "in" operator for lists is faster for successful searches

reset(); print c in s; show() # Early-out for matches.
# only 2 compares. identity implies equality

print('Predicted sort compares: %.1f' %(n*log(n,2)))
reset(); s.sort(); show()# Timsort takes advantage of partially sorted data, so it can do better than n*log(n)
reset(); s.sort(); show()# So, if data is already sorted, the cost is just verifying that it is sorted.

print 'Predicted bisect compares: %.1f' % (log(n,2))
reset(); bisect(s, a); show ()      # Both successful and unsuccessful searches take log n compares
reset(); bisect(s, b); show ()
reset(); bisect(s, c); show ()      # Identity doesn't help because we're looking for a range, not a value, calls .__lt__()
# Property: Success is cheaper than Failure

# Q. What is binary search good for? A. Searching ranges of values rather than specific values
# Q. Downsides? A. To get the savings, you have to pay for a sort first.

# >>> cuts = [60,70,80,90]
# >>> grades = 'FDCBA'
# >>> from bisect import bisect
# >>> grades[bisect(cuts, 50)]
# 'F'
# >>> grades[bisect(cuts, 65)]
# 'D'
# >>> grades[bisect(cuts, 671)]
# 'A'
# >>> grades[bisect(cuts, 71)]
# 'C'
# >>> [grades[bisect(cuts, score)] for score in [72,65,89,70,100,61,90,88,44,99,82]]
# ['C', 'D', 'B', 'C', 'A', 'D', 'A', 'B', 'F', 'A', 'B']


# Faster Way?
# >>> grade_table = [grades[bisect(cuts, score)] for score in range(101)]
# >>> grade_table
# ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']




## Study set (hashtable) searches ##########################
#abs(hash('raymond'))

data = map(Int, [10, 20, 30, 40, 20, 5, 10, 15, 20])
a = Int(11)
b = Int(20)
c = data[2]
n = len(data)

other_data = map(Int, [20, 30, 40, 300, 400, 500, 300]) + data[-4:]
t = set(other_data)

print '=' * 30
reset(); s = set(data); show() # Work at build a set: n calls to hash() and 1 compare per non-identical duplicate
reset(); print a in s; show()  # Cost of an unsuccessful search is 1 hash and 0 compares.
reset(); print b in s; show()  # Cost of a successful search is 1 hash and 1 compares.
reset(); print c in s; show()  # Cost of a successful identity search is 1 hash and 0 compares.

print '=' * 30
reset(); d = dict.fromkeys(s); show() # Cost of converting a set to a dict is 0 hashes and 0 compares.
reset(); u = s.copy(); show() # Cost of copying a set is 0 hashes and 0 compares.
reset(); u = s | t; show()  # Union, intersection, and difference cost 0 hashes and 1 compare per non-identical overlap
reset(); u = s & t; show()
reset(); u = s - t; show()

# Copying dict is about 1/5th as fast as list because it is about 5 times bigger for the same amount of data
# Dict needs more space to avoid hash collisions


## Immutability and hashability ##########################################

'''
Q. Why do we hash?
A. The same reason we use zip codes -- too reduce the search space

Q. Is there a risk?
A. Yes, if something reports the wrong zip code, you will look in the wrong place.

Q. Does our notion of equality matter?
A. It works as long as the zip codes match.

Hash invariant:

    If x == y, then hash(x) == hash(y)

Q. Do people sometimes mess this up?
A. Yes. They change equality and forget to update the hash.


'''

class CIStr(str):
    'Case insensitve string'

    def __eq__(self, other):
        return self.lower() == other.lower()

    # In order to keep equality working right for sets/dicts
    def __hash__(self):
        return hash(self.lower())

s = CIStr('RAYmond')
t = CIStr('RaymonD')
print {s, t}


class WitnessProtectionProgram(str):
    def __hash__(self):
        return randrange(1000000)

bg = WitnessProtectionProgram('Tony Soprano')
safe_house = {bg}

print bg in safe_house

#print bg in safe_house

class A:
    # Broken class
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return len(self.name)

    def set_name(self, name):
        self.name = name



# Homework: Exactly 15 minutes to review
# * Core Containers.PDF Summary slides
# * Review everything in instrument.py



# If something is hashable, it can be used as dict key or set element
# If something is mutable, its values can be changed with a public API

# Generally, we only put immutable objects in sets

#hash([]) doesn't work

a = A('matthew')
s = {a}
a in s# returns True
a.set_name('matt')
a in s# returns False


class HashableList(list):
    '''Don't do this. anti-pattern'''
    def __hash__(self):
        return hash(tuple(self))
c = HashableList([10,20,30])
s = {c}
print c in s, '<-- expected to be true'
c.append(40)
print c in s, '<-- expected to be false'

class Person:
    'Legitimate use case for a mutable, hashable class'
    # hash on just the immutable portion

    def __init__(self, name, dragons=0):
        self._name = name
        self.dragons = dragons

    def __eq__(self, other):
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return 'Person({0}, {1} dragons)'.format(self._name, self.dragons)

d = Person('Danyres', dragons=3)
j = Person('Jon Snow')
w = Person('Ice King')

s = {d,j,w}
print(s)

d.dragons -= 1
w.dragons += 1
print(s)
print d in s
print w in s

# still there because the hash value is generated from the _name attr, not the entire class















