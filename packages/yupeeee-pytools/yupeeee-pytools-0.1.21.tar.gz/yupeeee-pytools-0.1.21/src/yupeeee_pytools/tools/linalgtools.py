import torch


__all__ = [
    "angle_of_three_points",
    "normalize_v",
    "proj_v1_to_v2",
    "orthogonal_vector_to_v",
]


def angle_of_three_points(
        start: torch.Tensor,
        mid: torch.Tensor,
        end: torch.Tensor,
        eps: float = 1e-6,
) -> torch.Tensor:
    v1 = start - mid
    v2 = end - mid

    v1 = v1 / torch.norm(v1)
    v2 = v2 / torch.norm(v2)

    angle = torch.dot(v1, v2)

    angle = angle.clip(-1, 1)

    if 1 - eps < angle < 1:
        angle = torch.Tensor([0])
    elif -1 < angle < -1 + eps:
        angle = torch.Tensor([torch.pi])
    else:
        angle = torch.acos(angle)

    return angle


def normalize_v(
        v: torch.Tensor,
        method: str = "unit",
) -> torch.Tensor:
    assert len(v.shape) == 1

    if method == "unit":
        return v / torch.norm(v)

    elif method == "dim":
        return v / torch.norm(v) * len(v) ** 0.5

    else:
        raise ValueError


def proj_v1_to_v2(
        v1: torch.Tensor,
        v2: torch.Tensor,
) -> torch.Tensor:
    assert len(v1.shape) == len(v2.shape) == 1

    v2_norm = torch.norm(v2)
    proj_norm = torch.dot(v1, v2) / v2_norm

    return v2 / v2_norm * proj_norm


def orthogonal_vector_to_v(
        v: torch.Tensor,
        seed: int = None,
) -> torch.Tensor:
    from .randtools import set_random_seed

    assert len(v.shape) == 1

    if seed is not None:
        set_random_seed(seed)

    rand_v = torch.rand_like(v)
    proj_v = proj_v1_to_v2(rand_v, v)

    return rand_v - proj_v
