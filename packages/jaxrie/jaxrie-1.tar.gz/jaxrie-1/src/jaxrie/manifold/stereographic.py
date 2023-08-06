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
filename : stereographic.py
project  : jaxrie
license  : GPL-3.0+

This is the universal model in stereographic projection.

Include Hyperbolic (Poincare) k < 0, Euclidean k = 0, and Spherical k > 0.
"""

# Standard Library
from functools import partial

# Types
from jax.typing import ArrayLike

# JAX
import jax

# Local
from .base import Manifold
from .math import (EPS, mobius_add, mobius_matmulh, mobius_matmull,
                   mobius_matmulr, mobius_matvec_mul, mobius_scala_mul,
                   stereo_egrad2rgrad, stereo_expmap, stereo_expmap0,
                   stereo_logmap, stereo_logmap0)

Array = jax.Array


class Stereographic(Manifold):
  """The universal Stereographic projection model."""

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def add(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Mobius addition on manifold with curvature k."""
    return mobius_add(x, y, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def sub(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Mobius subtraction on manifold with curvature k."""
    return mobius_add(x, -y, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def mul(r: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Mobius multiplication on manifold with curvature k."""
    return mobius_scala_mul(r, x, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def matvec(m: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Mobius matrix vector multiplication on manifold with curvature k."""
    return mobius_matvec_mul(m, x, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def matmul(x1: Array, x2: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Mobius matrix multiplication on manifold with curvature k."""
    return mobius_matmulh(x1, x2, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def matmull(x1: Array, x2: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Matrix multiplication (left H, right E) with curvature k."""
    return mobius_matmull(x1, x2, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def matmulr(x1: Array, x2: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Matrix multiplication (left E, right H) with curvature k."""
    return mobius_matmulr(x1, x2, k, eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def expmap(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Exponential map on manifold with curvature k."""
    return stereo_expmap(x, y, k, axis=-1, eps=eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def logmap(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Logarithm map on manifold with curvature k."""
    return stereo_logmap(x, y, k, axis=-1, eps=eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def expmap0(u: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Exponential map on manifold with curvature k."""
    return stereo_expmap0(u, k, axis=-1, eps=eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def logmap0(y: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Logarithm map on manifold with curvature k."""
    return stereo_logmap0(y, k, axis=-1, eps=eps)

  @staticmethod
  @partial(jax.jit, static_argnames=("eps",), inline=True)
  def egrad2rgrad(x: Array, grad: Array, k: ArrayLike, eps: float = EPS) -> Array:
    """Euclidean gradient to Riemannian gradient."""
    return stereo_egrad2rgrad(x, grad, k, eps=eps)
