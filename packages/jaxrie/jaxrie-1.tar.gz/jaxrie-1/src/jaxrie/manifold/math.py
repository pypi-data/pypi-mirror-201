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
filename : math.py
project  : jaxrie
license  : GPL-3.0+

Mathematical functions.

SH(sh) for Hypersphere and Hyperboloid (Lorentz model).

DP(stereo) for Project Hypersphere and Poincaré ball.
"""
# Standard Library
from collections.abc import Callable
from functools import partial

# Types
from jax.typing import ArrayLike
from typing import TypeVar, cast

# JAX
import jax
import jax.numpy as jnp

Array = jax.Array

EPS = 1e-15
HALF_EPS = 1e-7

FN = TypeVar("FN", bound=Callable)


@partial(jax.jit, static_argnames=("axis", "ids", "keepdims"), inline=True)
def select_dim(
    x: Array,
    axis: int,
    ids: tuple[int | None, int | None, int | None] | int,
    keepdims: bool = True,
) -> Array:
  """Select the dim-th dimension of x."""
  naxis = list(range(x.ndim))[axis]
  axes = isinstance(ids, tuple) and slice(*ids) or ids
  idx = max(naxis, 0) * (slice(None),) + (axes,) + (x.ndim - naxis - 1) * (slice(None),)
  if keepdims:
    return x[idx][..., None]
  return x[idx]


@partial(jax.jit, static_argnames=("eps",), inline=True)
def safe_div(x: Array, y: Array, eps: float = EPS) -> Array:
  """Safe division."""
  return jnp.divide(x, jnp.maximum(y, eps))


@partial(jax.jit, static_argnames=("eps",), inline=True)
def safe_sqrt(x: Array, eps: float = EPS) -> Array:
  """Safe square root."""
  return jnp.sqrt(jnp.maximum(x, eps))


@partial(jax.jit, static_argnames=("eps",), inline=True)
def safe_arctanh(x: Array, eps: float = HALF_EPS) -> Array:
  """Safe arctanh."""
  return jnp.arctanh(jnp.clip(x, -1 + eps, 1 - eps))


@partial(jax.jit, static_argnames=("eps",), inline=True)
def radius(k: ArrayLike, eps: float = EPS) -> Array:
  """Radius with curvature k in ."""
  return jnp.reciprocal(safe_sqrt(jnp.abs(k), eps=eps))


@partial(jax.jit, static_argnames=("eps",), inline=True)
def origin(k: ArrayLike, eps: float = EPS) -> Array:
  """Origin of x."""
  return safe_sqrt(radius(k, eps=eps), eps=eps)


@partial(jax.jit, static_argnames=("size",), inline=True)
def sh_metric(size: int, k: ArrayLike = -1.0) -> Array:
  """SH metric.

  k < 0: Lorentz   -1, 1, 1, ...
  other: Euclidean  1, 1, 1, ...
  """
  return jnp.ones(size).at[0].set(jnp.sign(k))


@partial(jax.jit, inline=True)
def sink(x: Array, k: ArrayLike) -> Array:
  """Sine function with curvature k."""
  k = jnp.asarray(k, dtype=x.dtype)
  return jax.lax.cond(
      k == 0,
      lambda: x,
      lambda: jax.lax.cond(
          k < 0,
          lambda: jnp.sinh(x),
          lambda: jnp.sin(x),
      ),
  )


@partial(jax.jit, inline=True)
def cosk(x: Array, k: ArrayLike) -> Array:
  """Cosine function with curvature k."""
  k = jnp.asarray(k, dtype=x.dtype)
  return jax.lax.cond(
      k == 0,
      lambda: x,
      lambda: jax.lax.cond(
          k < 0,
          lambda: jnp.cosh(x),
          lambda: jnp.cos(x),
      ),
  )


@partial(jax.jit, inline=True)
def tank(x: Array, k: ArrayLike) -> Array:
  """Tangent function with curvature k."""
  k = jnp.asarray(k, dtype=x.dtype)
  return jax.lax.cond(
      k == 0,
      lambda: x,
      lambda: jax.lax.cond(
          k < 0,
          lambda: jnp.tanh(x),
          lambda: jnp.tan(x),
      ),
  )


@partial(jax.jit, inline=True)
def arctank(x: Array, k: ArrayLike) -> Array:
  """Arctangent function with curvature k."""
  k = jnp.asarray(k, dtype=x.dtype)
  return jax.lax.cond(
      k == 0,
      lambda: x,
      lambda: jax.lax.cond(
          k < 0,
          lambda: jnp.arctanh(x),
          lambda: jnp.arctan(x),
      ),
  )


@partial(jax.jit, inline=True)
def arcsink(x: Array, k: ArrayLike) -> Array:
  """Arcsine function with curvature k."""
  k = jnp.asarray(k, dtype=x.dtype)
  return jax.lax.cond(
      k == 0,
      lambda: x,
      lambda: jax.lax.cond(
          k < 0,
          lambda: jnp.arcsinh(x),
          lambda: jnp.arcsin(x),
      ),
  )


@partial(jax.jit, inline=True)
def arccosk(x: Array, k: ArrayLike) -> Array:
  """Arccosine function with curvature k."""
  k = jnp.asarray(k, dtype=x.dtype)
  return jax.lax.cond(
      k == 0,
      lambda: x,
      lambda: jax.lax.cond(
          k < 0,
          lambda: jnp.arccosh(x),
          lambda: jnp.arccos(x),
      ),
  )


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def lambda_x(x: Array, k: ArrayLike, axis: int = -1, keepdims: bool = False) -> Array:
  """Calculate the conformal factor."""
  return 2 / (1 + k * sqnorm(x, axis=axis, keepdims=keepdims))


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def inner(x: Array, y: Array, axis: int = -1, keepdims: bool = False) -> Array:
  """Inner product of two vectors."""
  if x.ndim == 0:
    x = x[None]
  return jnp.sum(x * y, axis=axis, keepdims=keepdims)


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def tangent_inner(
    x: Array, u: Array, v: Array, k: ArrayLike, axis: int = -1, keepdims: bool = False
) -> Array:
  """Inner product of two tangent vectors."""
  return (lambda_x(x, k, axis=axis, keepdims=keepdims) ** 2) * inner(
      u, v, axis=axis, keepdims=keepdims
  )


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def minkowski_inner(
    x: Array, y: Array, k: ArrayLike = -1.0, axis: int = -1, keepdims: bool = False
) -> Array:
  """Minkowski inner product of two vectors."""
  xy = x * y
  if xy.ndim == 0:
    xy = xy[None]
  g = sh_metric(xy.shape[axis], k=k)
  return jnp.sum(g * xy, axis=axis, keepdims=keepdims)


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def sqnorm(x: Array, axis: int = -1, keepdims: bool = False) -> Array:
  """Squared norm of a vector."""
  if x.ndim == 1:
    x = x[None]
  return inner(x, x, axis=axis, keepdims=keepdims)


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def tangent_sqnorm(
    x: Array, u: Array, k: ArrayLike, axis: int = -1, keepdims: bool = False
) -> Array:
  """Squared norm of a tangent vector."""
  return tangent_inner(x, u, u, k, axis=axis, keepdims=keepdims)


@partial(jax.jit, static_argnames=("axis", "keepdims"), inline=True)
def minkowski_sqnorm(
    x: Array, k: ArrayLike = -1.0, axis: int = -1, keepdims: bool = False
) -> Array:
  """Squared norm of a vector in Minkowski space."""
  if x.ndim == 1:
    x = x[None]
  return minkowski_inner(x, x, k=k, axis=axis, keepdims=keepdims)


@partial(jax.jit, static_argnames=("axis", "keepdims", "eps"), inline=True)
def norm(x: Array, axis: int = -1, keepdims: bool = False, eps: float = EPS) -> Array:
  """Norm of a vector."""
  return safe_sqrt(sqnorm(x, axis=axis, keepdims=keepdims), eps=eps)


@partial(jax.jit, static_argnames=("axis", "keepdims", "eps"), inline=True)
def tangent_norm(
    x: Array,
    u: Array,
    k: ArrayLike,
    axis: int = -1,
    keepdims: bool = False,
    eps: float = EPS,
) -> Array:
  """Norm of a tangent vector."""
  return lambda_x(x, k, axis=axis, keepdims=keepdims) * norm(
      u, axis=axis, keepdims=keepdims, eps=eps
  )


@partial(jax.jit, static_argnames=("axis", "keepdims", "eps"), inline=True)
def minkowski_norm(
    x: Array,
    k: ArrayLike = -1.0,
    axis: int = -1,
    keepdims: bool = False,
    eps: float = EPS,
) -> Array:
  """Norm of a vector in Minkowski space."""
  return safe_sqrt(minkowski_sqnorm(x, k=k, axis=axis, keepdims=keepdims), eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_add(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius addition of two vectors x.y in manifold with curvature k."""
  sqnx = k * sqnorm(x, axis=-1, keepdims=True)
  sqny = k * sqnorm(y, axis=-1, keepdims=True)
  xy = k * inner(x, y, axis=-1, keepdims=True)
  num = (1 - 2 * xy - sqny) * x + (1 + sqnx) * y
  denom = 1 - 2 * xy + sqnx * sqny
  return safe_div(num, denom, eps=eps)


# TODO
@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_adde(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius addition of two vectors x(in H) & y(in E) in manifold with curvature k."""
  return stereo_expmap(x, stereo_ptrans0(x, y, k, eps=eps), k, eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_scala_mul(alpha: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius multiplication of a vector by a scalar in manifold with curvature k."""
  c = radius(k, eps=eps)
  x_norm = norm(x, axis=-1, keepdims=True, eps=eps) / c
  return tank(alpha * arctank(x_norm, k), k) * x / x_norm


@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_matvec_mul(m: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius multiplication of a matrix by a vector in manifold with curvature k."""
  if x.ndim > 1:
    raise ValueError("x must be a vector, use mobius_matmul instead.")
  axis = -1
  c = radius(k, eps=eps)
  x_norm = norm(x, axis=axis, keepdims=True, eps=eps)
  mx = m @ x
  mx_norm = norm(mx, axis=axis, keepdims=True, eps=eps)

  res = c * tank((mx_norm / x_norm) * arctank(x_norm / c, k), k) * mx / mx_norm
  # NOTE: why qual to zero?
  return cast(
      Array,
      jnp.where(
          jnp.prod(mx == 0, axis=axis, keepdims=True),
          jnp.zeros_like(res),
          res,
      ),
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_matmulh(x1: Array, x2: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius matrix multiplication in H with curvature k."""
  return stereo_expmap0(
      stereo_logmap0(x1, k, eps=eps) @ stereo_logmap0(x2, k, eps=eps), k, eps=eps
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_matmull(x1: Array, x2: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius matrix multiplication (left H, right E) with curvature k."""
  axis = -1
  c = radius(k, eps=eps)
  x_norm = norm(x1, axis=axis, keepdims=True, eps=eps)
  xx = x1 @ x2
  xx_norm = norm(xx, axis=axis, keepdims=True, eps=eps)

  res = c * tank((xx_norm / x_norm) * arctank(x_norm / c, k), k) * xx / xx_norm
  # NOTE: why qual to zero?
  return cast(
      Array,
      jnp.where(
          jnp.prod(xx == 0, axis=axis, keepdims=True),
          jnp.zeros_like(res),
          res,
      ),
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_matmulr(x1: Array, x2: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Mobius matrix multiplication (left H, right E) with curvature k."""
  # return stereo_expmap0(x1 @ stereo_logmap0(x2, k, eps=eps), k, eps=eps)
  axis = -1
  c = radius(k, eps=eps)
  x_norm = norm(x2.swapaxes(-1, -2), axis=axis, keepdims=True, eps=eps)
  xx = x2.swapaxes(-1, -2) @ x1.swapaxes(-1, -2)
  xx_norm = norm(xx, axis=axis, keepdims=True, eps=eps)

  res = c * tank((xx_norm / x_norm) * arctank(x_norm / c, k), k) * xx / xx_norm
  # NOTE: why qual to zero?
  return cast(
      Array,
      jnp.where(
          jnp.prod(xx == 0, axis=axis, keepdims=True),
          jnp.zeros_like(res),
          res,
      ),
  ).swapaxes(-1, -2)


# TODO: implement mobius_left_matmul
# @partial(jax.jit, static_argnames=("eps",), inline=True)
def mobius_left_matmul(_m: Array, _x: Array, _k: ArrayLike, _eps: float = EPS) -> Array:
  """Mobius matrix multiplication in manifold with curvature k."""
  raise NotImplementedError


# def mobius_fn(fn: FN) -> FN:
#     """Mobius function composition in manifold with curvature k."""

#     def wrap(*args, **kwds) ->


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_add(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """SH addition of two vectors x.y in SH manifold with curvature k."""
  return sh_expmap(
      x,
      sh_ptrans0(x, sh_logmap0(y, k, eps=eps), k, eps=eps),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_adde(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """SH addition of two vectors x in L, y in E with curvature k."""
  return sh_expmap(
      x,
      sh_ptrans0(x, y, k, eps=eps),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_scalar_mul(m: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """SH mix space scalar multiplication with curvature k."""
  return sh_expmap0(
      m * sh_logmap0(x, k, eps=eps),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_matmulh(m: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """SH hyberbolic space matrix multiplication with curvature k."""
  return sh_expmap0(
      sh_logmap0(m, k, eps=eps) @ sh_logmap0(x, k, eps=eps),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_matmull(m: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """SH mix space matrix multiplication (left L, right E) with curvature k."""
  return sh_expmap0(
      sh_logmap0(m, k, eps=eps) @ x,
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_matmulr(m: Array, x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """SH mix space matrix multiplication (left E, right L) with curvature k."""
  return sh_expmap0(
      m @ sh_logmap0(x, k, eps=eps),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def gyration(u: Array, v: Array, a: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Gyration of a vector u around a vector v in manifold with curvature k."""
  return mobius_add(
      -mobius_add(u, v, k, eps=eps),
      mobius_add(u, mobius_add(v, a, k, eps=eps), k, eps=eps),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def stereo_proj(x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Project x on the manifold with curvature k."""
  c = radius(k, eps=eps)
  x_norm = norm(x, axis=-1, keepdims=True, eps=eps)
  return jax.lax.select(
      x_norm > jnp.full_like(x, c),
      c * x / x_norm,
      x,
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_proj(x: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Project x on the manifold with curvature k."""
  x_norm = minkowski_sqnorm(x, k=0, axis=-1, keepdims=True)
  return x.at[..., :1].set(safe_sqrt(x_norm - (1 / k), eps=eps))


@partial(jax.jit, static_argnames=("axis", "eps"), inline=True)
def stereo_dist(
    x: Array, y: Array, k: ArrayLike, axis: int = -1, eps: float = EPS
) -> Array:
  """Distance between two vectors in manifold with curvature k."""
  c = radius(k, eps=eps)
  return 2 * c * arctank(norm(mobius_add(-x, y, k, eps=eps), axis=axis, eps=eps) / c, k)


@partial(jax.jit, static_argnames=("axis", "eps"), inline=True)
def sh_dist(
    x: Array, y: Array, k: ArrayLike, axis: int = -1, eps: float = EPS
) -> Array:
  """Distance between two vectors in manifold with curvature k."""
  c = radius(k, eps=eps)
  return c * arccosk(k * minkowski_inner(x, y, k=k, axis=axis, keepdims=True), k)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def stereo_ptrans(
    x: Array, y: Array, v: Array, k: ArrayLike, eps: float = EPS
) -> Array:
  """Compute the parallel transport of v from x to y."""
  return (
      gyration(y, -x, v, k, eps=eps)
      * lambda_x(x, k, axis=-1, keepdims=True)
      / lambda_x(y, k, axis=-1, keepdims=True)
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def stereo_ptrans0(y: Array, v: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Compute the parallel transport of v from the origin to y."""
  return stereo_ptrans(jnp.zeros_like(y), y, v, k, eps=eps)


# @partial(jax.jit, static_argnames=("eps",), inline=True)
def _sh_ptrans_v1(
    x: Array, y: Array, v: Array, k: ArrayLike, eps: float = EPS
) -> Array:
  """Compute the parallel transport of v from x to y with curvature k."""
  logxy = sh_logmap(x, y, k, eps=eps)
  logyx = sh_logmap(y, x, k, eps=eps)
  return v - (
      minkowski_inner(logxy, v, k=k, axis=-1, keepdims=True)
      / (sh_dist(x, y, k, axis=-1) ** 2)
  ) * (logxy + logyx)


# @partial(jax.jit, static_argnames=("eps",), inline=True)
def _sh_ptrans(x: Array, y: Array, v: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Compute the parallel transport of v from x to y with curvature k."""
  return v - safe_div(
      k * minkowski_inner(y, v, k=k, axis=-1, keepdims=True),
      1 + k * minkowski_inner(x, y, k=k, axis=-1, keepdims=True),
      eps=eps,
  ) * (x + y)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_ptrans(x: Array, y: Array, v: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Compute the parallel transport of v from x to y with curvature k."""
  return jax.lax.cond(
      jnp.all(x == y),
      lambda: v,  # Avoild div 0
      lambda: _sh_ptrans(x, y, v, k, eps=eps),
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_ptrans0(y: Array, v: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Compute the parallel transport of v from the origin to y with curvature k."""
  c = radius(k, eps=eps)
  return sh_ptrans(jnp.zeros_like(y).at[..., 0].set(c), y, v, k, eps=eps)


@partial(jax.jit, static_argnames=("axis", "eps"), inline=True)
def stereo_expmap(
    x: Array, u: Array, k: ArrayLike, axis: int = -1, eps: float = EPS
) -> Array:
  """Exponential map of a tangent vector u at x in manifold with curvature k."""
  c = radius(k, eps=eps)
  return mobius_add(
      x,
      c
      * tank(tangent_norm(x, u, k, axis, keepdims=True, eps=eps) / 2 / c, k)
      * (u / norm(u, axis=axis, keepdims=True, eps=eps)),
      k,
      eps=eps,
  )


@partial(jax.jit, static_argnames=("axis", "eps"), inline=True)
def stereo_expmap0(u: Array, k: ArrayLike, axis: int = -1, eps: float = EPS) -> Array:
  """Exponential map at the origin."""
  return stereo_expmap(jnp.zeros_like(u), u, k, axis=axis, eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_expmap(x: Array, u: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Exponential map of a tangent vector u at x in L manifold with curvature k."""
  c = radius(k, eps=eps)
  u_norm = minkowski_norm(u, k=k, axis=-1, keepdims=True, eps=eps) / c
  return (cosk(u_norm, k) * x) + (sink(u_norm, k) * (u / u_norm))


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_expmap0(u: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Exponential map at the origin with curvature k."""
  c = radius(k, eps=eps)
  x = jnp.zeros_like(u).at[..., 0].set(c)
  u = u.at[..., 0].set(0)
  return sh_expmap(x, u, k, eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_expmap00(u: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Exponential map at the origin with 0 prepend with curvature k."""
  c = radius(k, eps=eps)
  u = jnp.concatenate([jnp.zeros_like(u[..., :1]), u], axis=-1)
  x = jnp.zeros_like(u).at[..., 0].set(c)
  return sh_expmap(x, u, k, eps=eps)


@partial(jax.jit, static_argnames=("axis", "eps"), inline=True)
def stereo_logmap(
    x: Array, y: Array, k: ArrayLike, axis: int = -1, eps: float = EPS
) -> Array:
  """Logarithmic map of a hyperbolic vector y at x in manifold with curvature k."""
  c = radius(k, eps=eps)
  sub = mobius_add(-x, y, k, eps=eps)
  return (
      2
      * c
      * arctank(norm(sub, axis=axis, keepdims=True, eps=eps) / c, k)
      * (sub / tangent_norm(x, sub, k, axis=axis, keepdims=True, eps=eps))
  )


@partial(jax.jit, static_argnames=("axis", "eps"), inline=True)
def stereo_logmap0(y: Array, k: ArrayLike, axis: int = -1, eps: float = EPS) -> Array:
  """Logarithmic map at the origin."""
  return stereo_logmap(jnp.zeros_like(y), y, k, axis=axis, eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_logmap(x: Array, y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Logarithmic map of a SH vector y at x in manifold with curvature k."""
  num = y - k * minkowski_inner(x, y, k=k, axis=-1, keepdims=True) * x
  return sh_dist(x, y, k, axis=-1, eps=eps) * (
      num / minkowski_norm(num, k=k, axis=-1, keepdims=True, eps=eps)
  )


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_logmap0(y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Logarithmic map at the origin with curvature k."""
  c = radius(k, eps=eps)
  x = jnp.zeros_like(y).at[..., 0].set(c)
  return sh_logmap(x, y, k, eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_logmap00(y: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Logarithmic map at the origin with 0 prepend with curvature k."""
  return sh_logmap0(y, k, eps=eps)[..., 1:]


@partial(jax.jit, static_argnames=("eps",), inline=True)
def stereo_egrad2rgrad(x: Array, grad: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Convert Euclidean gradient to Riemannian gradient."""
  return safe_div(grad, lambda_x(x, k, axis=-1, keepdims=True), eps=eps)


@partial(jax.jit, static_argnames=("eps",), inline=True)
def sh_egrad2rgrad(x: Array, grad: Array, k: ArrayLike, eps: float = EPS) -> Array:
  """Convert Euclidean gradient to Riemannian gradient."""
  del eps
  grad = grad.at[..., 0].mul(-1)
  return grad - minkowski_inner(x, grad, k=k, axis=-1, keepdims=True) * (x * k)


if __name__ == "__main__":
  x = jnp.arange(8, dtype="float32").reshape(2, 4) / 8
  y = jnp.arange(8, dtype="float32").reshape(4, 2) / 7.5
  assert jnp.allclose(stereo_logmap0(stereo_expmap0(x, 1.0), 1.0), x)
  assert jnp.allclose(sh_logmap0(sh_expmap0(x, 1.0)[..., 1:], 1.0), x[..., 1:])
