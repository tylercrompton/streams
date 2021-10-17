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

from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Container,
    Iterable,
    Iterator,
    Optional,
    TypeVar,
    Union,
)

__all__ = (
    'LinearStream',
    'Stream',
)

MT = TypeVar('MT')  # type of values after mapping
VT = TypeVar('VT')  # type of values before or without mapping


class Stream(Container[VT], metaclass=ABCMeta):
    __slots__: Iterable[str]

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

    @classmethod
    @abstractmethod
    def map(
            cls,
            fn: Callable[..., MT],
            *streams: Stream,
            does_memoize: bool=True
    ) -> Stream[MT]:
        ...


class LinearStream(Stream[VT], Iterable[VT], metaclass=ABCMeta):
    __slots__: Iterable[str]

    def __getitem__(
            self,
            key: Union[int, slice],
    ) -> Union[VT, LinearStream[VT]]:
        ...

    def __iter__(self) -> Iterator[VT]:
        ...

    @property
    @abstractmethod
    def next(self) -> Optional[LinearStream[VT]]:
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
            does_memoize: bool=True,
    ) -> Optional[LinearStream[VT]]:
        ...

    @classmethod
    @abstractmethod
    def _from_iterator(
            cls,
            iterator: Iterator[VT],
            does_memoize: bool=True,
    ) -> Optional[LinearStream[VT]]:
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
