import time

from .timeit import timeit


def test_timeit():

    @timeit
    def wait():
        time.sleep(1e-10)

    for _ in range(5):
        wait()
