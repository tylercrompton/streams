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

from math import pi
from operator import add, attrgetter, truediv
from pprint import pprint

from streams import SinglyLinkedStream as Stream

if __name__ == '__main__':
    numerators = Stream(
        4,
        lambda: Stream(-4, lambda: numerators)
    )
    denominators = Stream(
        1,
        lambda: Stream.map(lambda x: x + 2, denominators)
    )

    leibniz = Stream.map(truediv, numerators, denominators)
    print('The Leibniz sequence:')
    print(list(leibniz[:10]))
    print()

    partial_sums = Stream(
        leibniz.value,
        lambda: Stream.map(add, leibniz.next, partial_sums)
    )
    print('The partial sums of the Leibniz sequence:')
    print(list(partial_sums[:10]))
    print()

    def shanks_transformation(stream):
        s0 = stream.value
        s1 = stream.next.value
        s2 = stream.next.next.value
        denominator = s0 - s1 - (s1 - s2)

        return Stream(
            s1 if denominator == 0 else s2 - (s2 - s1) ** 2 / denominator,
            lambda: shanks_transformation(stream.next)
        )

    transformation = shanks_transformation(partial_sums)
    print(
        'The Shanks transformation of the partial sums of the Leibniz '
        'sequence:'
    )
    print(list(transformation[:10]))
    print()

    def make_tableau(transform, stream):
        return Stream(
            stream,
            lambda: make_tableau(transform, transform(stream))
        )

    tableau = make_tableau(shanks_transformation, partial_sums)
    print(
        'The tableau of successive Shanks transformations of the partial sums '
        'of the Leibniz sequence:'
    )
    pprint(list(tableau[:10]))
    print()

    acceleration = Stream.map(attrgetter('value'), tableau)
    print(
        'The first value of each stream in the tableau of successive Shanks '
        'transformations of the partial sums of the Leibniz sequence:'
    )
    print(list(acceleration[:10]))
    print()

    print('The value of the Leibniz series:')
    print(acceleration[59])
    print()

    print('The value of pi that is provided by math.pi:')
    print(pi)
