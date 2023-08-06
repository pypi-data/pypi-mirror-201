import torch

from .fcn import FCN


@torch.no_grad()
def test_fcn():
    bs = 2
    input_dim = 3
    output_dim = 4
    net_arch = [5, 6]
    m = FCN(input_dim=input_dim, output_dim=output_dim, net_arch=net_arch)

    x = torch.randn(bs, input_dim)
    y = m(x)

    assert y.shape == (bs, output_dim)
    assert len(m) == 1 + 2 * len(net_arch)
