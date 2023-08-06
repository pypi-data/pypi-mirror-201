import torch

from .config import *


__all__ = [
    "Footprint",
]


class Footprint:
    def __init__(
            self,
            model,
            step: int,
            method: str = default_method,
            normalize: str = default_normalize,
            seed: int = default_seed,
            bound_data: bool = False,
            use_cuda: bool = False,
    ) -> None:
        from .direction import DirectionGenerator

        self.model = model
        self.step = step
        self.method = method
        self.normalize = normalize
        self.seed = seed
        self.bound_data = bound_data
        self.use_cuda = use_cuda

        self.direction_generator = DirectionGenerator(
            method=method,
            normalize=normalize,
            seed=seed,
            model=model,
            use_cuda=use_cuda,
        )

    def __call__(
            self,
            data: torch.Tensor,
            epsilons: torch.Tensor,
            targets: torch.Tensor = None,
    ) -> torch.Tensor:
        directions = self.direction_generator(
            data=data,
            targets=targets,
        )

        footprints = []

        for i in range(len(data)):
            footprints.append(
                self.generate_footprints(
                    data=data[i],
                    direction=directions[i],
                    epsilon=epsilons[i],
                ).unsqueeze(dim=0)
            )

        return torch.cat(footprints, dim=0)

    def generate_footprints(
            self,
            data: torch.Tensor,
            direction: torch.Tensor,
            epsilon: float,
    ) -> torch.Tensor:
        from ..tools import repeat_tensor

        footprints = repeat_tensor(
            tensor=data,
            repeat=self.step + 1,
            dim=0,
        )
        footprints_shape = footprints.shape

        if epsilon < 0:
            return torch.ones_like(footprints) * invalid_footprint_val

        directions = repeat_tensor(
            tensor=direction,
            repeat=self.step + 1,
            dim=0,
        ).reshape(self.step + 1, -1)
        strides = torch.linspace(0., epsilon, self.step + 1)

        footprints += (directions.T * strides).T.reshape(footprints_shape)

        if self.bound_data:
            footprints = footprints.clamp(0, 1)

        return footprints
