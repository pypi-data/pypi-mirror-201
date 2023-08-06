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
filename : base.py
project  : jaxrie
license  : MIT

Manifold base.
"""
import jax
from jax.typing import ArrayLike
from abc import abstractmethod, ABCMeta

Array = jax.Array


class Manifold(metaclass=ABCMeta):
  """Manifold base."""

  @staticmethod
  @abstractmethod
  def add(x: Array, y: Array, k: ArrayLike, eps: float) -> Array:
    """Addition on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def sub(x: Array, y: Array, k: ArrayLike, eps: float) -> Array:
    """Subtraction on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def mul(r: Array, x: Array, k: ArrayLike, eps: float) -> Array:
    """Scala multiplication on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def matvec(m: Array, x: Array, k: ArrayLike, eps: float) -> Array:
    """Matrix vector multiplication on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def matmul(x1: Array, x2: Array, k: ArrayLike, eps: float) -> Array:
    """Matrix multiplication on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def matmull(x1: Array, x2: Array, k: ArrayLike, eps: float) -> Array:
    """Matrix multiplication (left H, right E) with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def matmulr(x1: Array, x2: Array, k: ArrayLike, eps: float) -> Array:
    """Matrix multiplication (left E, right H) with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def expmap(x: Array, y: Array, k: ArrayLike, eps: float) -> Array:
    """Exponential map on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def logmap(x: Array, y: Array, k: ArrayLike, eps: float) -> Array:
    """Logarithm map on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def expmap0(u: Array, k: ArrayLike, eps: float) -> Array:
    """Exponential map on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def logmap0(y: Array, k: ArrayLike, eps: float) -> Array:
    """Logarithm map on manifold with curvature k."""
    raise NotImplementedError

  @staticmethod
  @abstractmethod
  def egrad2rgrad(x: Array, grad: Array, k: ArrayLike, eps: float) -> Array:
    """Euclidean gradient to Riemannian gradient."""
    raise NotImplementedError
