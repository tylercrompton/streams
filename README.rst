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

Examples
========

If you want to dive straight into the code, feel free to peruse the
“examples/” directory.

First, let's import the :python:`SinglyLinkedStream` class.

::

    >>> from stream import SinglyLinkedStream as Stream

Next, we'll create a stream of ones.

::

    >>> ones = Stream(1, lambda: ones)
    >>> ones
    SinglyLinkedStream(1, <function <lambda> at 0x101c0a9d8>, does_memoize=True)

The first argument_ to the :python:`Stream` constructor is the value of the
node that :python:`ones` will refer to. The second argument is a thunk_ that
returns the next node.

To do the next step, we'll need to create a stream of the natural numbers.

::

   >>> from operator import add
   >>> ints = Stream(1, lambda: Stream.map(add, ones, ints))
   >>> ints
   SinglyLinkedStream(1, <function <lambda> at 0x10317cc80>, does_memoize=True)

Notice that we have been defining our streams with implicit recursion_. This is
common when working with streams as it makes code quite concise and allows for
powerful techniques. When we create a function_ in Python, a closure_ is
created, which contains that function and the defining environment. This allows
us to reference `free variables`_ (including those that have not yet been
defined) inside the function body from any enclosing scope.

But creating an indefinitely long stream of ones or natural numbers could
easily be done with built-in functions, standard library functions, or
generators. So let's get into the more interesting stuff.

Now, let's calculate π. We'll do this via the `Leibniz series`_. The most
straightforward way to do this is to create a stream for the numerators and a
stream for the denominators and then perform an element-wise division on them.

::

    >>> numerators = Stream(4, lambda: Stream(-4, lambda: numerators))
    >>> denominators = Stream(1, lambda: Stream.map(lambda x: x + 2, denominators))
    >>> from operator import truediv
    >>> leibniz = Stream.map(truediv, numerators, denominators)
    >>> list(leibniz[:10])
    [4.0, -1.3333333333333333, 0.8, -0.5714285714285714, 0.4444444444444444, -0.36363636363636365, 0.3076923076923077, -0.26666666666666666, 0.23529411764705882, -0.21052631578947367]

We now have a stream for the Leibniz sequence, but π is the *series*. How do we
programmatically take the sum of an infinite sequence? Unfortunately, we
can't—at least not without calculus. So our next best option is to take the sum
of some finite number of items.

To do that, let's create a stream for the partial sums where the item at index
``i`` is the summation of all of the numbers in the sequence up to and
including the item at index ``i``.

::

    >>> partial_sums = Stream(leibniz.cursor.value, lambda: Stream.map(add, leibniz[1:], partial_sums))
    >>> list(partial_sums[:10])
    [4.0, 2.666666666666667, 3.466666666666667, 2.8952380952380956, 3.3396825396825403, 2.9760461760461765, 3.2837384837384844, 3.017071817071818, 3.2523659347188767, 3.0418396189294032]

We now have a stream of approximations of π. Admittedly, we still haven't done
anything that can't easily be done in a fresh installation of Python. Now,
we'll see the true power of streams. In Python, an iterator can represent an
infinite number of values. But what it can't do is maintain its state when a
value is retrieved from it. Technically, you could duplicate an iterator via
|itertools.tee|_, but that's fairly cumbersome to use for what we're about to
do.

It turns out that the Leibniz sequence is very slow to converge. In fact, you'd
have to sum approximately 400,000 terms to obtain accuracy to six digits. It
would take far too long to calculate π to the maximum accuracy allowed by a
floating point number. Fear not. We can accelerate this sequence using one of
several `series acceleration`_ techniques. For this example, we'll use the
relatively simple `Shanks transformation`_. So let's get to it.

::

    >>> def shanks_transformation(stream):
    ...     s0 = stream.value
    ...     s1 = stream.next.value
    ...     s2 = stream.next.next.value
    ...     denominator = s0 - s1 - (s1 - s2)
    ...     return Stream(
    ...         s1 if denominator == 0 else s2 - (s2 - s1) ** 2 / denominator,
    ...         lambda: shanks_transformation(stream.next)
    ...     )
    ...
    >>> transformation = shanks_transformation(partial_sums)
    >>> list(transformation[:10])
    [3.166666666666667, 3.1333333333333337, 3.1452380952380956, 3.13968253968254, 3.1427128427128435, 3.1408813408813416, 3.142071817071818, 3.1412548236077655, 3.1418396189294033, 3.141406718496503]

The reasoning that our implementation of :python:`shanks_transformation`
slightly deviates from the formal definition of Shanks transformation is
outside the scope of the tutorial. But an important thing to note is that
despite our retrieval of downstream values, the original stream's state remains
intact, allowing us to get the next value of the transformation in the same
manner. Also note that our sequence is converging far more quickly than the
partial sums sequence was converging. We're getting closer.

It turns out that you can apply the Shanks transformation to the sequence
multiple times. You can do this as many times as you want. Due to restrictions
in Python, there exists a practical limit to how many times you can can do this
before causing a stack overflow, but we won't meet that limit in this example.

Next, let's create a tableau of successive transformations. In other words,
we'll create a stream of streams such that each successive stream will be the
transformation applied to the previous stream.

::

    >>> def make_tableau(transform, stream):
    ...     return Stream(
    ...         stream,
    ...         lambda: make_tableau(transform, transform(stream))
    ...     )
    ...
    >>> tableau = make_tableau(shanks_transformation, partial_sums)

Lastly, to get an idea of how quickly our sequence is now converging, let's
create a stream of the first value of each stream in the tableau.

::

    >>> acceleration = Stream.map(attrgetter('value'), tableau)
    >>> list(acceleration[:10])
    [4.0, 3.166666666666667, 3.142105263157895, 3.141599357319005, 3.1415927140337785, 3.1415926539752927, 3.1415926535911765, 3.141592653589778, 3.1415926535897953, 3.141592653589795]

As one can see, this accelerates quite quickly. In fact,
:python:`acceleration[59]` is the exact same value that |math.pi|_ provides.

::

    >>> acceleration[59]
    3.141592653589793
    >>> from math import pi
    >>> pi
    3.141592653589793

I'm not entirely certain as to how many iterations it would take to get this
level of precision in :python:`partial_sums`, but I believe it's somewhere on
the order of 500 quadrillion iterations. Sixty iterations is obviously much
better.

.. _abstract data type: https://en.wikipedia.org/wiki/Abstract_data_type
.. _argument: https://en.wikipedia.org/wiki/Parameter_(computer_programming)
.. _closure: https://en.wikipedia.org/wiki/Closure_(computer_programming)
.. _data structure: https://en.wikipedia.org/wiki/Data_structure
.. _free variables: https://en.wikipedia.org/wiki/Variable_(computer_science)
.. _function: https://en.wikipedia.org/wiki/Subroutine
.. _harmonic sequence: https://en.wikipedia.org/wiki/Harmonic_series_(mathematics)
.. _iterators: https://docs.python.org/3/glossary.html#term-iterator
.. |itertools.tee| replace:: :python:`itertools.tee`
.. _itertools.tee: https://docs.python.org/3/library/itertools.html#itertools.tee
.. _lazy evaluation: https://en.wikipedia.org/wiki/Lazy_evaluation
.. _Leibniz series: https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80
.. _linked list: https://en.wikipedia.org/wiki/Linked_list
.. |math.pi| replace:: :python:`math.pi`
.. _math.pi: https://docs.python.org/3/library/math.html#math.pi
.. |map| replace:: :python:`map`
.. _map: https://docs.python.org/3/library/functions.html#map
.. _natural numbers: https://en.wikipedia.org/wiki/Natural_number
.. _nodes: https://en.wikipedia.org/wiki/Node_(computer_science)
.. _Pythagorean triples: https://en.wikipedia.org/wiki/Pythagorean_triple
.. _recursion: https://en.wikipedia.org/wiki/Recursion_(computer_science)
.. _series acceleration: https://en.wikipedia.org/wiki/Series_acceleration
.. _Shanks transformation: https://en.wikipedia.org/wiki/Shanks_transformation
.. _streams: https://en.wikipedia.org/wiki/Stream_(computer_science)
.. |sys.stdout| replace:: :python:`sys.stdout``
.. _sys.stdout: https://docs.python.org/3/library/sys.html#sys.stdout
.. _tail recursion elimination: https://en.wikipedia.org/wiki/Tail_call
.. _thunk: https://en.wikipedia.org/wiki/Thunk
