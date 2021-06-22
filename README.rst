.. image:: https://readthedocs.org/projects/pystreams/badge/?version=latest
    :target: https://pystreams.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

=======
Streams
=======

.. role:: python(code)
   :language: python

If an `abstract data type`_ can be implemented with nodes_, then it can be
implemented via stream nodes.

The most powerful feature of streams_ is the ability to leverage `lazy
evaluation`_. For example, consider a stream of `natural numbers`_. The value
of the first node would be explicitly set to :python:`1` and the following
node, when needed, would be generated to hold the value of the previous node's
value incremented by one and to be able to generate the subsequent node in a
similar manner. Admittedly, this is a trivial example, but the point is to
express that streams can be self-referential.

One of the things that makes streams so capable is their ability to be
traversed multiple times without changing their internal structure. This is
unlike iterators_ which discard data as one iterates through them.

If you're unsure of which class to use, you probably want
:python:`SinglyLinkedStream`. For the sake of brevity, you might want to create
an alias for the class (e.g. :python:`Stream = SinglyLinkedStream`).

Installation
============

To-do

Documentation
=============

The documentation can be found at https://pystreams.readthedocs.io/. If you
prefer to view the documentation locally, you can build it from the source. To
build the documentation to HTML, navigate to the “docs/” directory and execute
the command ``make html``. The home page of the documentation will be at
“docs/build/html/index.html”. For a full list of possible formats in which the
documentation can be built, see “docs/Makefile” (or “docs/make.bat”).

License
=======

This project is licensed under the GNU General Public License, Version 3. See
“LICENSE.txt” for the full text of the license.

.. _abstract data type: https://en.wikipedia.org/wiki/Abstract_data_type
.. _iterators: https://docs.python.org/3/glossary.html#term-iterator
.. _lazy evaluation: https://en.wikipedia.org/wiki/Lazy_evaluation
.. _natural numbers: https://en.wikipedia.org/wiki/Natural_number
.. _nodes: https://en.wikipedia.org/wiki/Node_(computer_science)
.. _streams: https://en.wikipedia.org/wiki/Stream_(computer_science)
