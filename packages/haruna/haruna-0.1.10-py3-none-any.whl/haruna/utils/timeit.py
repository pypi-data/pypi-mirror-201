import time

import torch
from loguru import logger
from torchmetrics import MeanMetric


def sync_perf_counter():
    if torch.cuda.is_available():
        torch.cuda.synchronize()

    return time.perf_counter()


def timeit(func):
    mean = MeanMetric()

    def timed(*args, **kwargs):
        start = sync_perf_counter()
        output = func(*args, **kwargs)

        time = sync_perf_counter() - start
        mean.update(time)

        logger.debug('{} took {:.6f} seconds, mean: {:.6f} seconds.', func.__qualname__, time, mean.compute().float())
        return output

    return timed
