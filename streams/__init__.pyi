from typing import (
    Any,
    Callable,
    Generic,
    Iterator,
    Reversible,
)

from .abc import (
    LinearStream,
    MT,
    VT,
)

__all__ = (
    'DoublyLinkedStream',
    'SinglyLinkedStream',
    'thunk_init',
)


class SinglyLinkedStream(LinearStream, Generic[VT]):
    __slots__ = (
        'does_memoize',
        '_value',
        '_next',
        '_next_thunk',
    )

    def __init__(
            self,
            value: VT,
            next_thunk: Callable[[], SinglyLinkedStream[VT]],
            *,
            does_memoize: bool=True
    ) -> None:
        self.does_memoize = ...
        self._value = ...
        self._next = ...
        self._next_thunk = ...

    def __contains__(self, value: VT) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def next(self) -> SinglyLinkedStream[VT]:
        ...

    @property
    def value(self) -> VT:
        ...

    @value.setter
    def value(self, value: VT) -> None:
        ...

    def filter(
            self,
            predicate: Callable[[VT], bool]=None,
    ) -> SinglyLinkedStream[VT]:
        ...

    @classmethod
    def map(
            cls,
            fn: Callable[..., MT],
            *streams: SinglyLinkedStream,
            does_memoize: bool=True
    ) -> SinglyLinkedStream[MT]:
        ...

    @classmethod
    def _from_iterator(
            cls,
            iterator: Iterator[VT],
    ) -> SinglyLinkedStream[VT]:
        ...

    def _starter(self, n: int) -> SinglyLinkedStream[VT]:
        ...

    def _stepper(self, n: int) -> SinglyLinkedStream[VT]:
        ...

    def _stopper(self, n: int) -> SinglyLinkedStream[VT]:
        ...


class DoublyLinkedStream(SinglyLinkedStream, Reversible, Generic[VT]):
    __slots__ = (
        '_previous',
        '_previous_thunk',
    )

    def __init__(
            self,
            value: VT,
            next_thunk: Callable[[], DoublyLinkedStream[VT]],
            previous_thunk: Callable[[], DoublyLinkedStream[VT]]=None,
            *,
            does_memoize: bool=True
    ) -> None:
        super().__init__(value, next_thunk, does_memoize=does_memoize)
        self._previous = ...
        self._previous_thunk = ...

    def __reversed__(self) -> DoublyLinkedStream[VT]:
        ...

    @property
    def next(self) -> DoublyLinkedStream[VT]:
        ...

    @property
    def previous(self) -> DoublyLinkedStream[VT]:
        ...

    def filter(
            self,
            predicate: Callable[[VT], bool]=None,
    ) -> DoublyLinkedStream[VT]:
        ...

    @classmethod
    def map(
            cls,
            fn: Callable[..., MT],
            *streams: DoublyLinkedStream,
            does_memoize: bool=True
    ) -> DoublyLinkedStream[MT]:
        ...

    @classmethod
    def _from_iterator(
            cls,
            iterator: Iterator[VT],
            previous_thunk: Callable[
                [],
                DoublyLinkedStream[VT],
            ]=lambda: None,
    ) -> DoublyLinkedStream[VT]:
        ...

    def _starter(self, n: int) -> DoublyLinkedStream[VT]:
        ...

    def _stepper(self, n: int) -> DoublyLinkedStream[VT]:
        ...

    def _stopper(self, n: int) -> DoublyLinkedStream[VT]:
        ...


def thunk_init(
        thunk: Callable[[], VT],
        init: Callable[[Any], None],
) -> Callable[[], VT]:
    ...
