import sys
from unittest import TestCase
from x7.lib.annotations import tests
from x7.lib.capture import Capture


@tests(Capture)
class TestCapture(TestCase):
    @tests(Capture.__enter__)
    @tests(Capture.__exit__)
    @tests(Capture.__init__)
    @tests(Capture.stderr)
    @tests(Capture.stdout)
    def test_capture(self):
        with Capture() as cm:
            print('StdOut', file=sys.stdout)
            print('StdErr', file=sys.stderr)
        self.assertEqual('StdOut\n', cm.stdout())
        self.assertEqual('StdErr\n', cm.stderr())
