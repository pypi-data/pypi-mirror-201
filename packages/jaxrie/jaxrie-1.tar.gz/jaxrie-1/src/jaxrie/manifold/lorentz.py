#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Python ♡ Nasy.

    |             *         *
    |                  .                .
    |           .                              登
    |     *                      ,
    |                   .                      至
    |
    |                               *          恖
    |          |\___/|
    |          )    -(             .           聖 ·
    |         =\ -   /=
    |           )===(       *
    |          /   - \
    |          |-    |
    |         /   -   \     0.|.0
    |  NASY___\__( (__/_____(\=/)__+1s____________
    |  ______|____) )______|______|______|______|_
    |  ___|______( (____|______|______|______|____
    |  ______|____\_|______|______|______|______|_
    |  ___|______|______|______|______|______|____
    |  ______|______|______|______|______|______|_
    |  ___|______|______|______|______|______|____

author   : Nasy https://nasy.moe
date     : Mar 13, 2023
email    : Nasy <nasyxx+python@gmail.com>
filename : lorentz.py
project  : jaxrie
license  : GPL-3.0+

Lorentz model.
"""

from .base import Manifold
import jax
import jax.numpy as jnp
from jax.typing import ArrayLike
from functools import partial

Array = jax.Array


class Lorentz(Manifold):
    """Lorentz model."""

    @staticmethod
    @partial(jax.jit, inline=True)
    def add(x: Array, y: Array, k: ArrayLike) -> Array:
        """Addition on manifold with curvature k."""
        pass
