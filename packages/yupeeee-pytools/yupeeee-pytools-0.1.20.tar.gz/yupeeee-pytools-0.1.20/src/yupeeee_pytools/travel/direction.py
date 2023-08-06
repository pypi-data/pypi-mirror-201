import torch
import torch.nn as nn

from .config import methods, normalizations


__all__ = [
    "DirectionGenerator",
]


def normalize_direction(
        direction: torch.Tensor,
        method: str = "dim",
) -> torch.Tensor:
    from ..tools import normalize_v

    shape = direction.shape

    normalized = normalize_v(
        v=direction.reshape(-1),
        method=method,
    )

    return normalized.reshape(shape)


# def cw_direction(
#         data: torch.Tensor,
#         targets: torch.Tensor,
#         model,
#         normalize: str = None,
#         seed: int = None,
#         use_cuda: bool = False,
# ) -> torch.Tensor:
# TBD


def fgsm_direction(
        data: torch.Tensor,
        targets: torch.Tensor,
        model,
        normalize: str = None,
        seed: int = None,
        use_cuda: bool = False,
) -> torch.Tensor:
    from ..tools import set_random_seed

    assert model is not None

    if seed is not None:
        set_random_seed(seed)

    device = torch.device("cuda") if use_cuda else torch.device("cpu")

    data, targets = data.detach().to(device), targets.detach().to(device)
    data.requires_grad = True

    out = model(data)
    model.zero_grad()
    loss = nn.CrossEntropyLoss()(out, targets)
    loss.backward()

    with torch.no_grad():
        data_grad = data.grad.data

    direction = data_grad.sign().detach().cpu()

    if normalize is not None:
        direction = normalize_direction(direction, normalize)

    return direction


def random_direction(
        data: torch.Tensor,
        normalize: str = None,
        seed: int = None,
) -> torch.Tensor:
    from ..tools import set_random_seed

    if seed is not None:
        set_random_seed(seed)

    direction = torch.randn_like(data)

    if normalize is not None:
        direction = normalize_direction(direction, normalize)

    return direction


class DirectionGenerator:
    def __init__(
            self,
            method: str = "fgsm",
            normalize: str = "dim",
            seed: int = None,
            model=None,
            use_cuda: bool = False,
    ) -> None:
        assert method in methods
        assert normalize in normalizations

        self.method = method
        self.normalize = normalize
        self.seed = seed
        self.model = model
        self.use_cuda = use_cuda

    def __call__(
            self,
            data: torch.Tensor,
            targets: torch.Tensor = None,
    ) -> torch.Tensor:
        if self.method == "fgsm":
            assert self.model is not None

            return fgsm_direction(
                data=data,
                targets=targets,
                model=self.model,
                normalize=self.normalize,
                seed=self.seed,
                use_cuda=self.use_cuda,
            )

        elif self.method == "random":
            return random_direction(
                data=data,
                normalize=self.normalize,
                seed=self.seed,
            )

        else:
            raise ValueError

    def make_perpendicular(
            self,
            direction: torch.Tensor,
            seed: int = None,
    ) -> torch.Tensor:
        from ..tools import orthogonal_vector_to_v, set_random_seed

        shape = direction.shape
        _direction = orthogonal_vector_to_v(
            v=direction.reshape(-1),
            seed=seed,
        )

        set_random_seed(seed=self.seed)

        _direction = _direction.reshape(shape)

        if self.normalize is not None:
            _direction = normalize_direction(_direction, self.normalize)

        return _direction
