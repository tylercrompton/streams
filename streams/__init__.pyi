from enum import auto, Enum
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Reversible,
    TypeVar,
)

from .abc import (
    LinearStream,
)

__all__ = (
    'DoublyLinkedStream',
    'SinglyLinkedStream',
    'thunk_init',
)

MT = TypeVar('MT')  # type of values after mapping
VT = TypeVar('VT')  # type of values before or without mapping


class TraversalDirection(Enum):
    NEXT: TraversalDirection
    PREVIOUS: TraversalDirection


class SinglyLinkedStream(LinearStream[VT]):
    __slots__: Iterable[str]

    does_memoize: bool
    _value: VT
    _next: Optional[SinglyLinkedStream[VT]]
    _next_thunk: Callable[[], Optional[SinglyLinkedStream[VT]]]

    def __init__(
            self,
            value: VT,
            next_thunk: Callable[[], Optional[SinglyLinkedStream[VT]]],
            *,
            does_memoize: bool=True
    ) -> None:
        ...

    def __contains__(self, value: VT) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def next(self) -> Optional[SinglyLinkedStream[VT]]:
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
    ) -> Optional[SinglyLinkedStream[VT]]:
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
            does_memoize: bool=True,
    ) -> Optional[SinglyLinkedStream[VT]]:
        ...

    def _starter(self, n: int) -> SinglyLinkedStream[VT]:
        ...

    def _stepper(self, n: int) -> SinglyLinkedStream[VT]:
        ...

    def _stopper(self, n: int) -> Optional[SinglyLinkedStream[VT]]:
        ...


class DoublyLinkedStream(SinglyLinkedStream[VT], Reversible[VT]):
    __slots__: Iterable[str]

    _previous: Optional[DoublyLinkedStream[VT]]
    _previous_thunk: Callable[[], Optional[DoublyLinkedStream[VT]]]

    def __init__(
            self,
            value: VT,
            next_thunk: Callable[[], Optional[DoublyLinkedStream[VT]]],
            previous_thunk: Callable[[], Optional[DoublyLinkedStream[VT]]]=None,
            *,
            does_memoize: bool=True
    ) -> None:
        ...

    def __reversed__(self) -> DoublyLinkedStream[VT]:
        ...

    @property
    def next(self) -> Optional[DoublyLinkedStream[VT]]:
        ...

    @property
    def previous(self) -> Optional[DoublyLinkedStream[VT]]:
        ...

    def filter(
            self,
            predicate: Callable[[VT], bool]=None,
    ) -> Optional[DoublyLinkedStream[VT]]:
        ...

    @classmethod
    def map(
            cls,
            fn: Callable[..., MT],
            *streams: DoublyLinkedStream,
            does_memoize: bool=True
    ) -> DoublyLinkedStream[MT]:
        ...

    def _filter(
            self,
            predicate: Callable[[VT], bool],
            traversal_direction: TraversalDirection,
    ) -> Optional[SinglyLinkedStream[VT]]:
        ...

    @classmethod
    def _from_iterator(
            cls,
            iterator: Iterator[VT],
            previous_thunk: Callable[
                [],
                DoublyLinkedStream[VT],
            ]=lambda: None,
            does_memoize: bool=True
    ) -> Optional[DoublyLinkedStream[VT]]:
        ...

    def _starter(self, n: int) -> DoublyLinkedStream[VT]:
        ...

    def _stepper(self, n: int) -> DoublyLinkedStream[VT]:
        ...

    def _stopper(self, n: int) -> Optional[DoublyLinkedStream[VT]]:
        ...


def thunk_init(
        thunk: Callable[[], VT],
        init: Callable[[Any], None],
) -> Callable[[], VT]:
    ...
