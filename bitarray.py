''' Build a bitarray with an API similar to bytearray

List of techniques:
    - Pick out the n-th bit:           (x >> n) & 1
    - Set the n-th bit:                (1 << n) | x
    - Reset (unset) the n-th bit:      ~(1 << n) & x
    - Ceiling division:                -(n // -d)
    - Floor division and modulo:       divmod(n, d)

Model of bitarray built on a bytearray

     0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23      <= i or index
     ------------------------------|-------------------------------|------------------------------
     0   0   0   0   0   0   0   0 | 1   1   1   1   1   1   1   1 | 2   2   2   2   2   2   2   2      <== i // 8
     0   1   2   3   4   5   6   7 | 0   1   2   3   4   5   6   7 | 0   1   2   3   4   5   6   7      <== i % 8

'''

def ceiling_division(n, d):
    'Return n divided by d but rounded up if there is a remainder'
    return -(n // -d)

class BitArray:
    def __init__(self, numbits):
        self.numbits = numbits
        numbytes = ceiling_division(numbits, 8)
        self.data = bytearray(numbytes)

    def __len__(self):
        return self.numbits

    def __setitem__(self, index, value):
        if index < 0:
            index += len(self)# this is how negative indexing works!
        if index >= len(self) or index < 0:
            raise IndexError('bitarray index out of range')
        if not isinstance(value, int):
            raise TypeError('an integer is required')
        if value not in (0,1):
            raise ValueError('bit must be in range(0,2)')
        bytenum, bitnum = divmod(index, 8)
        mask = 1 << bitnum
        if value:
            self.data[bytenum] |= mask
        else:
            self.data[bytenum] &= ~mask

    def __getitem__(self, index):
        if index < 0:
            index += len(self)# this is how negative indexing works!
        if index >= len(self) or index < 0:
            raise IndexError('bitarray index out of range')

        bytenum, bitnum = divmod(index, 8)
        return (self.data[bytenum] >> bitnum) & 1

    def __repr__(self):
        # keep the printout to a reasonable size ~ <60 items
        size = min(30, len(self))
        bits = ''.join([str(self[i]) for i in range(size)])#map(str, self))
        if len(self) > size:
            bits += '...'
        return 'BitArray(%s)' % bits

if __name__ == '__main__':

    b = BitArray(20)
    print len(b)
    b[11] = 1
    b[13] = 1
    b[5] = 1
    b[6] = 1
    b[17] = 1
    b[13] = 0
    print [b[i] for i in range(20)]

