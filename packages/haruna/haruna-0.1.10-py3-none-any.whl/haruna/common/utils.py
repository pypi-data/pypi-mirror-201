# from https://github.com/DLR-RM/stable-baselines3/blob/master/stable_baselines3/common/utils.py

from itertools import zip_longest
from typing import Iterable

import numpy as np
import torch


def as_tensor(x, device: torch.device):
    if isinstance(x, np.ndarray):
        return torch.as_tensor(x, device=device)
    elif isinstance(x, dict):
        return {k: torch.as_tensor(v, device=device) for k, v in x.items()}
    else:
        raise ValueError(f'Unsupported type: {type(x)}')


def zip_strict(*iterables: Iterable) -> Iterable:
    r"""
    ``zip()`` function but enforces that iterables are of equal length.
    Raises ``ValueError`` if iterables not of equal length.
    Code inspired by Stackoverflow answer for question #32954486.

    :param \*iterables: iterables to ``zip()``
    """
    # As in Stackoverflow #32954486, use
    # new object for "empty" in case we have
    # Nones in iterable.
    sentinel = object()
    for combo in zip_longest(*iterables, fillvalue=sentinel):
        if sentinel in combo:
            raise ValueError("Iterables have different lengths")
        yield combo


@torch.no_grad()
def polyak_update(params: Iterable[torch.Tensor], target_params: Iterable[torch.Tensor], tau: float) -> None:
    """
    Perform a Polyak average update on ``target_params`` using ``params``:
    target parameters are slowly updated towards the main parameters.
    ``tau``, the soft update coefficient controls the interpolation:
    ``tau=1`` corresponds to copying the parameters to the target ones whereas nothing happens when ``tau=0``.
    The Polyak update is done in place, with ``no_grad``, and therefore does not create intermediate tensors,
    or a computation graph, reducing memory cost and improving performance.  We scale the target params
    by ``1-tau`` (in-place), add the new weights, scaled by ``tau`` and store the result of the sum in the target
    params (in place).
    See https://github.com/DLR-RM/stable-baselines3/issues/93

    Args:
        params (Iterable[torch.Tensor]): parameters to use to update the target params
        target_params (Iterable[torch.Tensor]): parameters to update
        tau (float): the soft update coefficient ("Polyak update", between 0 and 1)
    """
    # zip does not raise an exception if length of parameters does not match.
    for param, target_param in zip_strict(params, target_params):
        target_param.data.mul_(1 - tau)
        torch.add(target_param.data, param.data, alpha=tau, out=target_param.data)
