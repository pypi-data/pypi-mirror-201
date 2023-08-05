import time
from unittest import TestCase
from x7.lib.annotations import tests
from x7.lib.timer import Timer


@tests(Timer)
class TestTimer(TestCase):
    @tests(Timer.__enter__)
    @tests(Timer.__exit__)
    @tests(Timer.__init__)
    def test___init__(self):
        # __init__(self, tag='Timer')
        t = Timer('test timer')
        with t:
            time.sleep(0.1)
        self.assertGreater(t.elapsed, 0.01)
