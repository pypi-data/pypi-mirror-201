from typing import List
from typing import Optional

import torch.nn as nn


class FCN(nn.Sequential):

    def __init__(self, input_dim: int, output_dim: Optional[int] = None, net_arch: List[int] = [64]):
        """Fully connected neural network.
        Args:
            input_dim (int): Input dimension.
            output_dim (Optional[int], optional): Output dimension. Defaults to None.
            net_arch (List[int], optional): Network architecture. Defaults to [64].
        """

        layers = []

        in_features = input_dim
        for hidden_dim in net_arch:
            layers += [
                nn.Linear(in_features=in_features, out_features=hidden_dim),
                nn.ReLU(inplace=True),
            ]
            in_features = hidden_dim

        if output_dim is not None:
            layers += [nn.Linear(in_features=in_features, out_features=output_dim)]

        super(FCN, self).__init__(*layers)
