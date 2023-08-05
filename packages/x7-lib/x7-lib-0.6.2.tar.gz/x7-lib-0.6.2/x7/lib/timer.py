import time


class Timer(object):
    """
        Timer class to be used in :code:`with` statement::

            with Timer('example'):
                for n in range(1024):
                    math.sqrt(n)
    """
    def __init__(self, tag='Timer'):
        self.tag = tag
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time_ns()
        print('%s: %s ms' % (self.tag, self.elapsed))

    @property
    def elapsed(self) -> float:
        """Total time in seconds. Only valid after :code:`with` block"""
        return (self.end - self.start) / 1000000000.0
