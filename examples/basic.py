# This file is part of Streams.
#
# Streams is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# Streams is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Streams.  If not, see <https://www.gnu.org/licenses/>.

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
