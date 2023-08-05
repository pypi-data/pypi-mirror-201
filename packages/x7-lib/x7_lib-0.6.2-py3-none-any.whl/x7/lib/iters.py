"""
Additional iterators ala itertools
"""

from itertools import islice, cycle as iter_cycle
from typing import Iterable, Collection, Union, Tuple

__all__ = ['iter_rotate', 't_range', 'xy_iter', 'xy_flatten']


def t_range(steps, t_start=0.0, t_end=1.0, closed=True, closed_start=True):
    """
        Floating point range().  (Think time range or theta range).

        :param steps:   Number of steps in the open range.  t_range(2) -> [0, 0.5, 1.0]
        :param t_start: Starting point of range
        :param t_end:   End of range.  Can be less than t_low.  t_range(2, 0, -1) -> [0, -0.5, -1.0]
        :param closed:  True to include end point.  t_range(2, closed=False) -> [0, 0.5]
        :param closed_start: True to include start point t_range(2, closed_start=False) -> [0.5, 1.0]
        :returns: generator

        Example::

            >>> list(t_range(10))
            [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            >>> list(t_range(10,2,1,False,False))
            [1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1]
    """
    t_len = t_end - t_start
    start = 0 if closed_start else 1
    end = steps+1 if closed else steps
    return (step / steps * t_len + t_start for step in range(start, end))


def iter_rotate(data: Union[str, Collection, Iterable], elems=2, offset=0, cycle=True) -> Iterable:
    """
        Return tuples of data, *rotating* around the end of the list.

        :param data:    list or string or other iterable
        :param elems:   number of elements per tuple
        :param offset:  starting offset
        :param cycle:   cycle back to start
        :returns: iterator

        Examples::

            >>> list(iter_rotate("abc"))
            [('a', 'b'), ('b', 'c'), ('c', 'a')]
            >>> list(iter_rotate("abcd", elems=3, offset=1))
            [('b', 'c', 'd'), ('c', 'd', 'a'), ('d', 'a', 'b'), ('a', 'b', 'c')]
            >>> list(iter_rotate("abcd", elems=3, offset=1, cycle=False))
            [('b', 'c', 'd'), ('c', 'd', 'a'), ('d', 'a', 'b')]

        Draw a triangle between three points::

            for (x1, y1), (x2, y2) in iter_rotate([(0, 0), (1, 0), (0, 1)]):
                line(x1, y1, x2, y2)
    """
    offset = offset % len(data)
    offset_end = (offset+len(data)) if cycle else (offset+len(data)-1)
    return zip(*(islice(iter_cycle(data), idx+offset, idx+offset_end) for idx in range(elems)))


def xy_iter(iterable: Iterable[float]) -> Iterable[Tuple[float, float]]:
    """
        Convert [x, y, x2, y2...] to [(x, y), (x2, y2)...].  Inverse of xy_flatten()::

            >>> list(xy_iter([1, 2, 3, 4]))
            [(1, 2), (3, 4)]
    """

    unique = object()
    it = iter(iterable)
    for x in it:
        y = next(it, unique)
        if y is unique:
            raise ValueError('Missing y value at end of iterable')
        yield x, y


def xy_flatten(iterable: Iterable[Iterable[float]]) -> Iterable[float]:
    """
        Flatten [(x, y)...] to [x, y, ...].  Inverse of xy_iter()::

            >>> list(xy_flatten([(1, 2), (3, 4, 5)]))
            [1, 2, 3, 4, 5]

        Note: This will actually flatten any iterable of iterables, but the
        intent is just for graphical things like (1, 2) or Point(3, 4).
    """

    return (v for xy in iterable for v in xy)
