import sys
from io import StringIO
from typing import Optional, Tuple, TextIO

TupleTextIO = Optional[Tuple[TextIO, TextIO]]
TupleStringIO = Optional[Tuple[StringIO, StringIO]]


class Capture(object):
    """
        Capture :code:`stdout` and :code:`stderr` for use in testing.

        Example::

            with Capture() as cap:
                something()
            self.assertIn('important', cap.stdout())
    """

    def __init__(self):
        self.old: TupleTextIO = None
        self.new: TupleStringIO = None

    def __enter__(self):
        self.old = sys.stderr, sys.stdout
        self.new = StringIO(), StringIO()
        sys.stderr, sys.stdout = self.new
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr, sys.stdout = self.old

    def stderr(self):
        """Return captured :code:`stderr` output as a string"""
        return self.new[0].getvalue()

    def stdout(self):
        """Return captured :code:`stdout` output as a string"""
        return self.new[1].getvalue()
