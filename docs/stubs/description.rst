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

.. _abstract data type: https://en.wikipedia.org/wiki/Abstract_data_type
.. _iterators: https://docs.python.org/3/glossary.html#term-iterator
.. _lazy evaluation: https://en.wikipedia.org/wiki/Lazy_evaluation
.. _natural numbers: https://en.wikipedia.org/wiki/Natural_number
.. _nodes: https://en.wikipedia.org/wiki/Node_(computer_science)
.. _streams: https://en.wikipedia.org/wiki/Stream_(computer_science)