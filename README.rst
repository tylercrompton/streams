..
    This file is part of Streams.

    Streams is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    Streams is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
    details.

    You should have received a copy of the GNU General Public License along
    with Streams.  If not, see <https://www.gnu.org/licenses/>.

.. image:: https://readthedocs.org/projects/pystreams/badge/?version=latest
    :target: https://pystreams.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

=======
Streams
=======

.. role:: python(code)
   :language: python
   :class: highlight

Streams is a library to facilitate the use of collections in a way that
simulates `lazy evaluation`_. This allows for powerfully concise code for
dynamically building potentially indefinitely large collections. For example,
one can construct the `Fibonacci sequence`_ in “one” line as follows:

.. code-block:: python

    from operator import add
    from streams import SinglyLinkedStream as Stream
    fib = Stream(0, lambda: Stream(1, lambda: Stream.map(add, fib, fib.next)))

If an `abstract data type`_ can be implemented via nodes_, then it can be
implemented via stream nodes.

One of the things that makes streams so capable is their ability to be
traversed multiple times without changing their internal structure. This is
unlike iterators_ which discard data as one iterates through them.

If you're unsure of which class to use, you probably want
:python:`SinglyLinkedStream`. For the sake of brevity, you might want to create
an alias for the class (e.g. :python:`Stream = SinglyLinkedStream`).

Installation
============

To do

Documentation
=============

The documentation can be found at https://pystreams.readthedocs.io/. If you
prefer to view the documentation locally, you can build it from the source. To
build the documentation to HTML, navigate to the “docs/” directory and execute
the command ``make html``. The home page of the documentation will be at
“docs/build/html/index.html”. For a full list of possible formats in which the
documentation can be built, see “docs/Makefile” (or “docs/make.bat”).

Contributing
============

The code conventions used throughout this project can be found in PEP 8 and PEP
257. Before submitting a pull request, please be sure that it corresponds to an
issue. If no such issue exists, then please create one.

License
=======

This project is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

.. _abstract data type: https://en.wikipedia.org/wiki/Abstract_data_type
.. _iterators: https://docs.python.org/3/glossary.html#term-iterator
.. _Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number
.. _lazy evaluation: https://en.wikipedia.org/wiki/Lazy_evaluation
.. _natural numbers: https://en.wikipedia.org/wiki/Natural_number
.. _nodes: https://en.wikipedia.org/wiki/Node_(computer_science)
.. _streams: https://en.wikipedia.org/wiki/Stream_(computer_science)
