# See README.rst at the top level directory of this repository for an
# explanation of the code.

from operator import add

from streams import SinglyLinkedStream as Stream

if __name__ == '__main__':
    ones = Stream(1, lambda: ones)
    print('Stream of ones:')
    print(list(ones[:10]))
    print()

    ints = Stream(1, lambda: Stream.map(add, ones, ints))
    print(ints)
    print('Stream of natural numbers:')
    print(list(ints[:10]))
