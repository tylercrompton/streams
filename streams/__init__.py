"""If an abstract data type can be implemented with nodes, then it can
be implemented via streams.

Before reading further, one needs to understand that the streams in this
package also serve the purpose of individual nodes. That is, a stream is
a node and a node is a stream. This decision was made for the sake of
efficiency and simplicity. When discussing this package, care shall be
taken to use the most conceptually proper term to deter confusion.

The most powerful feature of streams is the ability to use lazy
evaluation. For example, consider a stream of natural numbers. The value
of the first node could be provided explicitly, the ``next`` property on
that node could be provided as the previous node's value incremented by
one, and so on and so forth. Admittedly, this is a trivial example, but
the point is to express how streams are capable of numerous tasks.

One of the things that makes streams so capable is that one can traverse
them multiple times without changing their internal structure. This is
unlike iterators which discard data as one iterates through them.

If you're unsure of which class to use, then you probably want
``SinglyLinkedStream``. For the sake of brevity, you might want to create
an alias for the class (e.g. ``Stream = SinglyLinkedStream``).

.. caution::
   Be very careful to not mix stream node types within a stream. It is
   assumed that all nodes within the simulated data structure are
   compatible. For example, it is incorrect to assume that a singly
   linked stream node will behave like a doubly linked stream node.

.. note::
   Note that this module has a few limitations due to Python's lack of
   tail recursion elimination. With that said, care has been taken to
   avoid this issue where possible.
"""

from collections.abc import Reversible
from enum import auto, Enum
from operator import attrgetter

from .abc import LinearStream

__all__ = (
    'DoublyLinkedStream',
    'SinglyLinkedStream',
    'thunk_init',
)


def reversed_node(node):
    try:
        return reversed(node)
    except TypeError:
        return node


class TraversalDirection(Enum):
    NEXT = auto()
    PREVIOUS = auto()


class SinglyLinkedStream(LinearStream):
    """A singly linked list class implemented as a stream. This is the
    most commonly used stream type.
    """

    __slots__ = (
        'does_memoize',
        '_value',
        '_next',
        '_next_thunk',
    )

    def __init__(self, value, next_thunk, *, does_memoize=True):
        """value is the value of the stream node.

        next_thunk is a zero-argument function that should return the
        following node.

        By default, the node will cache the result of next_thunk. This
        can potentially hog a lot of memory. To turn caching off, set
        does_memoize to False. It might be desirable to propagate this
        to composite streams generated by custom functions.

        Changing any of these values after initialization may cause
        unexpected results.
        """

        self._value = value
        self._next_thunk = next_thunk
        self.does_memoize = does_memoize

    def __contains__(self, value):
        """Determines whether value is in the stream. Use with caution
        as this will not terminate if the stream is infinite.
        """

        return value in iter(self)

    def __repr__(self):
        """Returns the canonical string representation of the stream
        node.
        """

        return '{}({}, {}, does_memoize={})'.format(
            self.__class__.__name__,
            repr(self._value),
            repr(self._next_thunk),
            repr(self.does_memoize),
        )

    @property
    def next(self):
        """Returns the next node."""

        try:
            return self._next
        except AttributeError:
            next_ = self._next_thunk()

            if self.does_memoize:
                self._next = next_

            return next_

    @property
    def value(self):
        """Returns the value of the node."""

        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of the node."""

        self._value = value

    def filter(self, predicate=None):
        """Returns a new stream that filters out the values that do not
        satisfy the predicate.

        predicate is the predicate to apply to the values in the
        stream. It defaults to testing each value itself for
        validity.
        """

        if predicate is None:
            def predicate(value):
                return bool(value)

        node = self

        while not predicate(node.value):
            node = node.next

            if node is None:
                return node

        return self.__class__(
            node._value,
            lambda: node.next.filter(predicate),
            does_memoize=node.does_memoize,
        )

    @classmethod
    def map(cls, fn, *streams, does_memoize=True):
        """Returns a new stream that contains the return values of the
        function applied to each item in the streams.

        fn is the function to be applied to each value in the stream.

        streams is the tuple of streams that contain the values to be
        mapped.

        By default, the node will cache the result of next_thunk. This
        can potentially hog a lot of memory. To turn caching off, set
        does_memoize to False. It might be desirable to propagate this
        to composite streams generated by custom functions.
        """

        return cls(
            fn(*map(attrgetter('value'), streams)),
            lambda: cls.map(
                fn,
                *map(attrgetter('next'), streams),
                does_memoize=does_memoize,
            ),
            does_memoize=does_memoize,
        )

    def _starter(self, n):
        """Returns the node that is n nodes away from self."""

        node = self

        for _ in range(n):
            node = node.next

            if node is None:
                raise IndexError('node index out of range.')

        return node

    def _stepper(self, n):
        """Returns a new stream that skips every n - 1 nodes."""

        def step(node, i):
            try:
                node = node._starter(i)
            except IndexError:
                return None

            return node._stepper(i)

        return self.__class__(
            self._value,
            lambda: step(self, n),
            does_memoize=self.does_memoize,
        )

    def _stopper(self, n):
        """Returns a new stream that is limited to n nodes."""

        def stop(node, i):
            next_ = node.next

            if next_ is None:
                if i > 1:
                    raise IndexError('node index out of range.')

                return None

            return next_._stopper(i - 1)

        if n == 0:
            return None
        else:
            return self.__class__(
                self._value,
                lambda: stop(self, n),
                does_memoize=self.does_memoize,
            )

    @classmethod
    def _from_iterator(cls, iterator, does_memoize=True):
        """Returns a new stream that contains data from an iterator. Use
        of the iterator elsewhere afterward is generally inadvisable.
        Otherwise, the stream might become out of sync.

        iterator is the iterator that will be used to retrieve the
        values for the stream.

        By default, the node will cache the result of next_thunk. This
        can potentially hog a lot of memory. To turn caching off, set
        does_memoize to False. It might be desirable to propagate this
        to composite streams generated by custom functions.
        """

        try:
            return cls(
                next(iterator),
                lambda: cls._from_iterator(iterator),
                does_memoize=does_memoize,
            )
        except StopIteration:
            return None


class DoublyLinkedStream(SinglyLinkedStream, Reversible):
    __slots__ = (
        '_previous',
        '_previous_thunk',
    )

    def __init__(
            self,
            value,
            next_thunk,
            previous_thunk=None,
            *,
            does_memoize=True
    ):
        """value is the value of the stream node.

        next_thunk is a zero-argument function that should return the
        following node.

        previous_thunk is a zero-argument function that should return
        the preceding node. It defaults to behaving similarly to singly
        linked nodes.

        By default, the node will cache the result of next_thunk. This
        can potentially hog a lot of memory. To turn caching off, set
        does_memoize to False. It might be desirable to propagate this
        to composite streams generated by custom functions.

        Changing any of these values after initialization may cause
        unexpected results.
        """

        super().__init__(value, next_thunk, does_memoize=does_memoize)

        if previous_thunk is None:
            def previous_thunk():
                return None

        self._previous_thunk = previous_thunk

    def __contains__(self, value):
        """Determines whether value is in the stream. Use with caution
        as this will not terminate if the stream is infinite.
        """

        for candidate in self:
            if candidate == value:
                return True

        for candidate in reversed(self).next:
            if candidate == value:
                return True

        return False

    def __repr__(self):
        """Returns the canonical string representation of the node."""

        return '{}({}, {}, {}, does_memoize={})'.format(
            self.__class__.__name__,
            repr(self._value),
            repr(self._next_thunk),
            repr(self._previous_thunk),
            repr(self.does_memoize)
        )

    def __reversed__(self):
        """Returns the stream in reverse."""

        if self.does_memoize:
            def next_init(obj):
                try:
                    obj._previous = node
                except AttributeError:
                    pass

            def previous_init(obj):
                try:
                    obj._next = node
                except AttributeError:
                    pass

            node = self.__class__(
                self.value,
                thunk_init(
                    lambda: reversed_node(self.previous),
                    next_init,
                ),
                thunk_init(
                    lambda: reversed_node(self.next),
                    previous_init,
                ),
                does_memoize=True,
            )

            return node

        return self.__class__(
            self.value,
            lambda: reversed_node(self.previous),
            lambda: reversed_node(self.next),
            does_memoize=False,
        )

    @property
    def next(self):
        """Returns the next node."""

        try:
            return self._next
        except AttributeError:
            next_ = self._next_thunk()

            if self.does_memoize:
                self._next = next_

            return next_

    @property
    def previous(self):
        """Returns the previous node."""

        try:
            return self._previous
        except AttributeError:
            previous = self._previous_thunk()

            if self.does_memoize:
                self._previous = previous

            return previous

    @property
    def value(self):
        """Returns the value of the node."""

        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of the node."""

        self._value = value

    def filter(self, predicate=None):
        """Returns a new stream that filters out the values that do not
        satisfy the predicate.

        predicate is the predicate to apply to the values in the
        stream. It defaults to testing each value itself for validity.
        """

        if predicate is None:
            def predicate(value):
                return value

        return self._filter(predicate, TraversalDirection.NEXT)

    @classmethod
    def map(cls, fn, *streams, does_memoize=True):
        """Returns a new stream that contains the return values of the
        function applied to each item in the streams.

        fn is the function to be applied to each value in the stream.

        streams is the tuple of streams that contain the values to be
        mapped.

        By default, the node will cache the result of next_thunk. This
        can potentially hog a lot of memory. To turn caching off, set
        does_memoize to False. It might be desirable to propagate this
        to composite streams generated by custom functions.
        """
        if does_memoize:
            def next_init(obj):
                obj._previous = node

            def previous_init(obj):
                obj._next = node

            node = cls(
                fn(*map(attrgetter('value'), streams)),
                thunk_init(
                    lambda: cls.map(
                        fn,
                        *map(attrgetter('next'), streams),
                        does_memoize=True,
                    ),
                    next_init,
                ),
                thunk_init(
                    lambda: cls.map(
                        fn,
                        *map(attrgetter('previous'), streams),
                        does_memoize=True,
                    ),
                    previous_init,
                ),
                does_memoize=True,
            )

            return node

        return cls(
            fn(*map(attrgetter('value'), streams)),
            lambda: cls.map(
                fn,
                *map(attrgetter('next'), streams),
                does_memoize=False,
            ),
            lambda: cls.map(
                fn,
                *map(attrgetter('previous'), streams),
                does_memoize=False,
            ),
            does_memoize=False,
        )

    def _filter(self, predicate, traversal_direction):
        """Returns a new stream that filters out the values that do not
        satisfy the predicate.

        predicate is the predicate to apply to the values in the
        stream. It defaults to testing each value itself for
        validity.

        traversal_direction is the direction in which the nodes should
        be traversed.
        """

        node = self

        attribute = 'next'
        if traversal_direction == TraversalDirection.PREVIOUS:
            attribute = 'previous'

        while not predicate(node.value):
            node = getattr(node, attribute)

            if node is None:
                return None

        if node.does_memoize:
            def next_init(obj):
                obj._previous = new_node

            def previous_init(obj):
                obj._next = new_node

            new_node = node.__class__(
                node.value,
                thunk_init(
                    lambda: node.next._filter(
                        predicate,
                        TraversalDirection.NEXT,
                    ),
                    next_init,
                ),
                thunk_init(
                    lambda: node.previous._filter(
                        predicate,
                        TraversalDirection.PREVIOUS,
                    ),
                    previous_init,
                ),
                does_memoize=True,
            )

            return new_node

        return self.__class__(
            node.value,
            lambda: node.next._filter(
                predicate,
                TraversalDirection.NEXT,
            ),
            lambda: node.previous._filter(
                predicate,
                TraversalDirection.PREVIOUS,
            ),
            does_memoize=False,
        )

    @classmethod
    def _from_iterator(cls, iterator, previous_thunk=None, does_memoize=True):
        """Returns a new stream that contains data from an iterator. Use
        of the iterator elsewhere afterward is generally inadvisable.
        Otherwise, the stream might become out of sync.

        iterator is the iterator that will be used to retrieve the
        values for the stream.

        previous_thunk is a zero-argument function that should return
        the preceding node. It defaults to behaving similarly to singly
        linked nodes.
        """

        if previous_thunk is None:
            def previous_thunk():
                return None

        try:
            value = next(iterator)
        except StopIteration:
            return cls()

        node = cls(
            value,
            lambda: cls._from_iterator(
                iterator,
                lambda: node,
                does_memoize=does_memoize,
            ),
            previous_thunk,
            does_memoize=does_memoize,
        )

        return node

    def _starter(self, n):
        """Returns the node that is n nodes away from self."""

        node = self
        attribute = 'next'

        if n < 0:
            n = abs(n)
            attribute = 'previous'

        for _ in range(abs(n)):
            node = getattr(node, attribute)

            if node is None:
                raise IndexError('node index out of range.')

        return node

    def _stepper(self, n):
        """Returns a new stream that skips every n - 1 nodes."""

        def step_forward(cursor, offset):
            try:
                cursor = cursor._starter(offset)
            except IndexError:
                return None

            return cursor._stepper(n)

        def step_backward(cursor, offset):
            try:
                cursor = cursor._starter(-offset)
            except IndexError:
                return None

            return cursor._stepper(n)

        if self.does_memoize:
            def next_init(obj):
                try:
                    obj._previous = node
                except AttributeError:
                    pass

            def previous_init(obj):
                try:
                    obj._next = node
                except AttributeError:
                    pass

            node = self.__class__(
                self._value,
                thunk_init(
                    lambda: step_forward(self, n),
                    next_init,
                ),
                thunk_init(
                    lambda: step_backward(self, n),
                    previous_init,
                ),
                does_memoize=self.does_memoize,
            )

            return node

        return self.__class__(
            self._value,
            lambda: step_forward(self, n),
            lambda: step_backward(self, n),
            does_memoize=self.does_memoize,
        )

    def _stopper(self, n):
        """Returns a new stream that is limited to n nodes."""

        if n == 0:
            return None

        if self.does_memoize:
            def next_init(obj):
                try:
                    obj._previous = node
                except AttributeError:
                    pass

            def previous_init(obj):
                try:
                    obj._next = node
                except AttributeError:
                    pass

            node = self.__class__(
                self._value,
                thunk_init(
                    lambda: self.next._stopper(n - 1),
                    next_init,
                ),
                thunk_init(
                    lambda: self.previous._stopper(n + 1),
                    previous_init,
                ),
                does_memoize=True,
            )

            return node

        return self.__class__(
            self._value,
            lambda: self.next._stopper(n - 1),
            lambda: self.previous._stopper(n + 1),
            does_memoize=False,
        )


def thunk_init(thunk, init):
    """Initializes the object returned by a thunk and wraps it into a
    new thunk. This is useful when working with thunks that can't or
    shouldn't be changed.

    thunk is the function that returns the object of interest.

    init is the function that initializes the return value of thunk.
    """

    def get_object():
        """Calls the thunk from the thunk_init call that created this
        function and and initializes the thunk's return value. See the
        docstring for thunk_init for more information.
        """

        obj = thunk()
        init(obj)

        return obj

    return get_object
