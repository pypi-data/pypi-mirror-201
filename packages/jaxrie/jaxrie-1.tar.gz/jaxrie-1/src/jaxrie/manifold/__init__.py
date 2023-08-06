# Local
from .base import Manifold
from .stereographic import Stereographic

stereographic = Stereographic()


__all__ = [
    "Manifold",
    "Stereographic",
    "stereographic",
]
