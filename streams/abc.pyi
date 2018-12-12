from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Container,
    Generic,
    Iterable,
    Iterator,
    TypeVar,
    Union,
)

__all__ = (
    'LinearStream',
    'Stream',
)

MT = TypeVar('MT')  # type of values after mapping
VT = TypeVar('VT')  # type of values before or without mapping


class Stream(Container, Generic[VT], metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def __contains__(self, value: VT) -> bool:
        ...

    def __repr__(self) -> str:
        ...

    @property
    @abstractmethod
    def value(self) -> VT:
        ...

    @value.setter
    @abstractmethod
    def value(self, value: VT) -> None:
        ...

    @abstractmethod
    def map(self, fn: Callable[[VT], MT]) -> Stream[MT]:
        ...


class LinearStream(Stream, Iterable, Generic[VT], metaclass=ABCMeta):
    __slots__ = ()

    def __getitem__(
            self,
            key: Union[int, slice],
    ) -> Union[VT, LinearStream[VT]]:
        ...

    def __iter__(self) -> Iterator[VT]:
        ...

    def filter(
            self,
            predicate: Callable[[VT], bool]=None,
    ) -> LinearStream[VT]:
        ...

    @classmethod
    def from_iterable(
            cls,
            iterable: Iterable[VT],
    ) -> LinearStream[VT]:
        ...

    @classmethod
    @abstractmethod
    def _from_iterator(
            cls,
            iterator: Iterator[VT],
    ) -> LinearStream[VT]:
        ...

    @abstractmethod
    def _starter(self, n: int) -> LinearStream[VT]:
        ...

    @abstractmethod
    def _stepper(self, n: int) -> LinearStream[VT]:
        ...

    @abstractmethod
    def _stopper(self, n: int) -> LinearStream[VT]:
        ...
