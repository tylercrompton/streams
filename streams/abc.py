from abc import ABCMeta, abstractmethod
from collections.abc import Container, Iterable

__all__ = (
    'LinearStream',
    'Stream',
)


class Stream(Container, metaclass=ABCMeta):
    """An abstract base class for stream classes (i.e. an
    interface for robust objects that are capable of holding an
    indefinite amount of data). All stream classes should directly or
    indirectly derive from this class.
    """

    __slots__ = ()

    def __repr__(self):
        """Returns the canonical string representation of the node."""

        return '{}({})'.format(
            self.__class__.__name__,
            repr(self.value),
        )

    @property
    @abstractmethod
    def value(self):
        """Returns the value of the node."""

        raise NotImplementedError

    @value.setter
    @abstractmethod
    def value(self, value):
        """Sets the value of the node."""

        raise NotImplementedError

    @abstractmethod
    def map(self, fn):
        """Returns a new stream that contains the return values of the
        function applied to each item in the source stream.

        fn is the function to be applied to each value in the stream.
        """

        raise NotImplementedError


class LinearStream(Stream, Iterable, metaclass=ABCMeta):
    """An abstract linearly linked list class implemented as a stream
    class.
    """

    __slots__ = ()

    def __getitem__(self, key):
        """Returns the value contained at a particular index or the
        items contained within a particular slice.

        key must be an integer or a slice object whose start and stop
        values are integers. Negative indices are relative to self.
        """

        if isinstance(key, int):
            return self._starter(key).value

        start, stop, step = key.start, key.stop, key.step

        node = self

        if start is not None:
            if start < 0:
                raise ValueError(
                    'start must be nonnegative integer, not {}'.format(
                        start)
                )

            node = node._starter(start)

        if stop is not None:
            if stop < 0:
                raise ValueError(
                    'stop must be nonnegative integer, not {}'.format(stop)
                )

            if start is not None:
                stop -= start

                if start > stop:
                    raise ValueError(
                        'start must be less than or equal to stop'
                    )

            node = node._stopper(stop)

        if step is not None:
            if step <= 0:
                raise ValueError(
                    'step must be positive integer, not {}'.format(step)
                )

            node = node._stepper(step)

        return node

    def __iter__(self):
        """Returns an iterator that yields the values from the stream.
        """

        node = self

        while node is not None:
            yield node.value
            node = node.next

    @abstractmethod
    def filter(self, predicate=None):
        """Returns a new stream that filters out the values that do not
        satisfy the predicate.

        predicate is the predicate to apply to the values in the
        stream. It defaults to testing each value itself for
        validity.
        """

        raise NotImplementedError

    @classmethod
    def from_iterable(cls, iterable):
        """Returns a new stream that contains data from an iterable. Use
        of the iterable elsewhere afterward is generally inadvisable.
        Otherwise, the stream might become out of sync.

        iterable is the iterable from which to create the stream.
        """

        return cls._from_iterator(iter(iterable))

    @classmethod
    @abstractmethod
    def _from_iterator(cls, iterator):
        """Returns a new stream that contains data from an iterator. Use
        of the iterator elsewhere afterward is generally inadvisable.
        Otherwise, the stream might become out of sync.

        iterator is the iterator that will be used to retrieve the
        values for the stream.
        """

        raise NotImplementedError

    @abstractmethod
    def _starter(self, n):
        """Returns the node that is n nodes away from self."""

        raise NotImplementedError

    @abstractmethod
    def _stepper(self, n):
        """Returns a new stream that skips every n - 1 nodes."""

        raise NotImplementedError

    @abstractmethod
    def _stopper(self, n):
        """Returns a new stream that is limited to n nodes."""

        raise NotImplementedError
